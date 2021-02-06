from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=20, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name

class Stock(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
	item_name = models.CharField(max_length=20, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	created_by = models.CharField(max_length=30, blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	request_quantity = models.IntegerField(default='0', blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	export_to_CSV = models.BooleanField(default=False)

	def __str__(self):
		return self.item_name

class StockHistory(models.Model):
	stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=20, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

	def __str__(self):
		return 'Purchase History for' + ' ' + self.stock.item_name


class StockRequestHistory(models.Model):
	stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True)
	request_quantity = models.IntegerField(default='0', blank=True, null=True)
	request_by = models.CharField(max_length=20, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	approval1 = models.CharField(max_length=20, blank=True, null=True)
	approved_by = models.CharField(max_length=20, blank=True, null=True)

	def __str__(self):
		return 'Stock Request History for ' + self.stock.item_name

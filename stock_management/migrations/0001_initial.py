# Generated by Django 2.0.7 on 2021-02-06 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('created_by', models.CharField(blank=True, max_length=30, null=True)),
                ('receive_quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('request_quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('reorder_level', models.IntegerField(blank=True, default='0', null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stock_management.Category')),
            ],
        ),
        migrations.CreateModel(
            name='StockHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('receive_quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('receive_by', models.CharField(blank=True, max_length=20, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('stock', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stock_management.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='StockRequestHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_quantity', models.IntegerField(blank=True, default='0', null=True)),
                ('request_by', models.CharField(blank=True, max_length=20, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('approval1', models.CharField(blank=True, max_length=20, null=True)),
                ('approved_by', models.CharField(blank=True, max_length=20, null=True)),
                ('stock', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stock_management.Stock')),
            ],
        ),
    ]

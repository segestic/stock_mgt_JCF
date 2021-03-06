from django import forms
from .models import Stock, Category

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        ############
        # for instance in Stock.objects.all():
        #     if instance.category == category:
        #         raise forms.ValidationError(str(category) + ' is already created')
        return category


    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    # item_name  = forms.ModelChoiceField(queryset=Stock.objects.all())
    # item_name  = forms.ModelChoiceField(queryset=Stock.objects.filter(category_id=))

    class Meta:
        model = Stock
        fields = ['category', 'item_name']
#
# ########seg
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             ####
#
#             category1 = self['category'].value()
#             if (category1 != ''):
#                 item_name  = forms.ModelChoiceField(queryset=Stock.objects.filter(category_id=category1))

class SearchForm(forms.Form):
    search = forms.CharField(help_text="Type to Search")


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required')
        ##########
        for instance in Category.objects.all():
            if instance.name == name:
                raise forms.ValidationError(str(name) + ' is already created')
        return name

# def clean_name(self):
    #     print(type(self.cleaned_data))
    #     name = self.cleaned_data.get('name')
    #
    #     with open("HSS/names.txt", 'r') as f:
    #         names = f.read().splitlines()
    #
    #     for whatever in names:
    #         if whatever in name:
    #             raise forms.ValidationError("You're trying to SPAM ME with %s" % whatever)
    #     return name

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['request_quantity']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']


class MakeRequestForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

# class MakeRequestForm1(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['category', 'item_name']
#
# #initialize
#     def __init__(self, *args, **kwargs):
#         #use super args because arguments gotten from parant class
#         super().__init__(*args, **kwargs)
#         #on first initialize the queryset should be gotten from the city object but none should be initialized
#         # self.fields['item_name'].queryset = Stock.objects.none(
#         self.fields['item_name'].queryset = Stock.objects.filter(item_name)
#         if 'category' in self.data:
#             # category = self.data.get('category')
#             item_name = self.data.get('item_name')
#             self.fields['item_name'].queryset = Stock.objects.filter(item_name)
#
# #if country is selected in the genrated queryset
#         if 'category' in self.data:
#             try:
#                 #id of the country(foreign/parent) should be integer of country
#                 category_id = int(self.data.get('category'))
#                 #filter the particiular city of the country selected above into the city queryset
#                 self.fields['item_name'].queryset = Stock.objects.filter(category_id=category_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#             # getting id of country by primary key instead of above geetting by integer i.e int(*.get('country')
#         # elif self.instance.pk:
#         #     #Model.Objects.filer == i.e equivalent to self.instance.Model. - etc
#         #     self.fields['item_name'].queryset = self.instance.cou.city_set.order_by('name')
from django import forms
from .models import CostFormData
from .models import Category, CategoryItem, ItemSize, SizePrice, MachineCost


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class CategoryItemForm(forms.ModelForm):
    class Meta:
        model = CategoryItem
        fields = ['category', 'name', 'description']

class ItemSizeForm(forms.ModelForm):
    class Meta:
        model = ItemSize
        fields = ['item', 'name', 'description']

class SizePriceForm(forms.ModelForm):
    class Meta:
        model = SizePrice
        fields = ['size', 'price', 'user']

class MachineCostForm(forms.ModelForm):
    class Meta:
        model = MachineCost
        fields = ['total_cost', 'details']

class CostForm(forms.ModelForm):
    class Meta:
        model = CostFormData
        fields = ['data', 'update_existing']
        widgets = {
            'data': forms.HiddenInput(),
            'update_existing': forms.CheckboxInput(),
        }

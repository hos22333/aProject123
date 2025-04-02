from django.contrib import admin
from .models import Category, CategoryItem, ItemSize, SizePrice, MachineCost, CostFormData

admin.site.register(Category)
admin.site.register(CategoryItem)
admin.site.register(ItemSize)
admin.site.register(SizePrice)
admin.site.register(MachineCost)
admin.site.register(CostFormData)

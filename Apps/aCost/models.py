from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CategoryItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ItemSize(models.Model):
    item = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, related_name="sizes")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.item.name} - {self.name}"

class SizePrice(models.Model):
    size = models.ForeignKey(ItemSize, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.size} - {self.price}"

class MachineCost(models.Model):
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Machine Cost: {self.total_cost}"

class CostFormData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    update_existing = models.BooleanField(default=False)

    def __str__(self):
        return f"Cost Data by {self.user.username} on {self.created_at}"

















class AutoFillConfig(models.Model):
    project_type = models.CharField(max_length=50)
    category_id = models.IntegerField()
    row_number = models.IntegerField()
    item = models.ForeignKey(CategoryItem, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(ItemSize, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('project_type', 'category_id', 'row_number')
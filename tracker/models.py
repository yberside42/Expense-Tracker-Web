from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User


PAYMENT_METHODS = (
    ("cash", "Efectivo"), 
    ("card", "Tarjeta"), 
    ("transfer", "Transferencia"), 
    ("other", "Otro"), )

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="uniq_category_owner_name")
        ]
    def __str__(self):
        return self.name 
    
class Expense(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))],)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="expenses")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cash",)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="expenses")
    
    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
    
    def __str__(self):
        return f"{self.date} · {self.category} · {self.amount}"
    

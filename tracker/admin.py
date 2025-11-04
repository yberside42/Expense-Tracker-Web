from django.contrib import admin
from .models import Category, Expense

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    list_display = ("name", "owner", "created_at")  
    list_filter = ("owner",)
    search_fields = ("name",)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin): 
    readonly_fields = ("created_at",)
    list_display = ("date", "category", "amount", "payment_method", "owner", "created_at")  # 👈
    list_filter = ("payment_method", "category", "owner", "date")
    search_fields = ("description",)
    date_hierarchy = "date"
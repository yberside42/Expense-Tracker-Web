from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("expenses/", views.expenses_list, name="expenses_list"),
    path("expenses/new/", views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/edit/", views.expense_update, name="expense_update"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    path("expenses/export/csv/", views.export_expenses_csv, name="expenses_export_csv"),
    path("expenses/export/json/", views.export_expenses_json, name="expenses_export_json"),

    path("categories/", views.categories_list, name="categories_list"),
    path("categories/new/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    path("reports/summary/", views.reports_summary, name="reports_summary"),

    path("signup/", views.signup, name="signup"),
]
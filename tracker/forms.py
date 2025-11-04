from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Expense

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        
    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Name can't empty")
        return name

class ExpenseForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        empty_label="---",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Expense
        fields = ["date", "amount", "category", "payment_method", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(owner=user).order_by("name")

    def clean_category(self):
        cat = self.cleaned_data["category"]
        if not self._user or cat.owner_id != self._user.id:
            raise forms.ValidationError("Categoría inválida.")
        return cat
    
    
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
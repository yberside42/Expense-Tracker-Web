from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from .models import Category, Expense
from .forms import CategoryForm, ExpenseForm, SignupForm
import csv 
import json

# Create your views here.d
def home(request):
    return redirect("expenses_list")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("expenses_list")  
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def expenses_list(request):
    qs = Expense.objects.select_related("category").filter(owner=request.user)
    category = request.GET.get("category") or ""
    query = request.GET.get("q") or ""
    start = request.GET.get("start") or ""
    end = request.GET.get("end") or ""
    order = request.GET.get("order") or "date"
    direction = request.GET.get("dir") or "desc"
    
    if category.isdigit():
        qs = qs.filter(category_id=int(category))
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    if query:
        qs = qs.filter(Q(description__icontains=query)) | Q(category__name__icontains=query)
    
    if order not in ("date", "amount"):
        order = "date"
    field = order if direction == "asc" else f"-{order}"
    qs = qs.order_by(field)
    
    paginator = Paginator(qs,10)
    page_object = paginator.get_page(request.GET.get("page"))
    
    ctx = {
        "page_obj": page_object,
        "expenses": page_object.object_list,
        "categories": Category.objects.filter(owner=request.user).order_by("name"),
        "current": {
            "category": category, "q": query,
            "start": start, "end": end,
            "order": order, "dir": direction,
        },
    }
    
    return render(request, "expense_list.html", ctx)  

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)   
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return redirect("expenses_list")
    else:
        form = ExpenseForm(user=request.user)                
    return render(request, "expense_form.html", {"form": form, "is_edit": False})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, owner=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, user=request.user)  
        if form.is_valid():
            form.save()
            return redirect("expenses_list")
    else:
        form = ExpenseForm(instance=expense, user=request.user)                
    return render(request, "expense_form.html", {"form": form, "is_edit": True})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, owner=request.user) 
    if request.method == "POST":
        expense.delete()
        return redirect("expenses_list")
    return render(request, "expense_confirm_delete.html", {"expense": expense})

@login_required
def categories_list(request):
    categories = Category.objects.filter(owner = request.user)
    return render(request, "category_list.html", {"categories": categories})

@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user  
            obj.save()
            return redirect("categories_list")
    else:
        form = CategoryForm()
    return render(request, "category_form.html", {"form": form, "is_edit": False})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "category_form.html", {"form": form, "is_edit": True})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, owner=request.user)  # 👈 no permite borrar de otro
    if request.method == "POST":
        category.delete()
        return redirect("categories_list")
    return render(request, "category_confirm_delete.html", {"category": category})

@login_required
def reports_summary(request):
    qs = Expense.objects.select_related("category").filter(owner=request.user)
    category = request.GET.get("category") or ""
    q = request.GET.get("q") or ""
    start = request.GET.get("start") or ""
    end = request.GET.get("end") or ""

    if category.isdigit():
        qs = qs.filter(category_id=int(category))
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    if q:
        qs = qs.filter(Q(description__icontains=q) | Q(category__name__icontains=q))

    summary = (
        qs.values("category__name")
          .annotate(total_amount=Sum("amount"), count=Count("id"))
          .order_by("category__name")
    )

    totals_by_month = (
        qs.annotate(month=TruncMonth("date"))
          .values("month")
          .annotate(total=Sum("amount"))
          .order_by("month")
    )

    ctx = {
        "categories": Category.objects.filter(owner=request.user).order_by("name"),
        "current": {"category": category, "q": q, "start": start, "end": end},
        "summary": summary,
        "totals_by_month": totals_by_month, 
    }
    return render(request, "reports_summary.html", ctx)

def filtered_expenses(request):
    qs = Expense.objects.select_related("category").filter(owner=request.user)
    category = request.GET.get("category") or ""
    q = request.GET.get("q") or ""
    start = request.GET.get("start") or ""
    end = request.GET.get("end") or ""
    order = request.GET.get("order") or "date"
    direction = request.GET.get("dir") or "desc"

    if category.isdigit():
        qs = qs.filter(category_id=int(category))
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    if q:
        qs = qs.filter(Q(description__icontains=q) | Q(category__name__icontains=q))
    if order not in ("date", "amount"):
        order = "date"
    field = order if direction == "asc" else f"-{order}"
    return qs.order_by(field)

@login_required
def export_expenses_csv(request):
    qs = filtered_expenses(request)
    response = HttpResponse(content_type = "text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename = "expenses.csv"'
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(["date", "amount", "category", "payment_method", "description"])
    
    for e in qs:
        writer.writerow([e.date, f"{e.amount}", e.category.name if e.category_id else "",
                         e.get_payment_method_display(), (e.description or "").replace("\n", " ").strip(),])
    return response

@login_required
def export_expenses_json(request):
    qs = filtered_expenses(request)  

    data = []
    for e in qs:
        data.append({
            "date": str(e.date),
            "amount": float(e.amount),
            "category": e.category.name if e.category_id else None,
            "payment_method": e.payment_method,
            "payment_method_display": e.get_payment_method_display(),
            "description": e.description or "",
        })

    payload = json.dumps(data, ensure_ascii=False, indent=2)

    response = HttpResponse(
        payload,
        content_type="application/json; charset=utf-8"
    )
    response["Content-Disposition"] = 'attachment; filename="expenses.json"'
    return response
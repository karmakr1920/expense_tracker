from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense, Category,User,MonthlyBudget
from django.db.models import Sum,Count
from django.contrib import messages
import calendar
from django.utils.timezone import now, timedelta
from datetime import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if password1 != password2:
            messages.warning(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        # login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('login')

    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('user_dashboard')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'registration/login.html')

def index(request):
    return render(request, 'tracker/index.html')


@login_required(login_url='/login/')
def user_dashboard(request):
    user = request.user
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    expenses = Expense.objects.filter(user=user,
                                      paid_date__year=current_year,
                                      paid_date__month=current_month)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Fetch user's monthly budget for current month/year
    try:
        monthly_budget_obj = MonthlyBudget.objects.get(user=user, year=current_year, month=current_month)
        monthly_budget = monthly_budget_obj.amount
    except MonthlyBudget.DoesNotExist:
        monthly_budget = 0  # Or default value, maybe 0 or None

    remaining_budget = monthly_budget - total_expenses

    # Paginate: 6 expenses per page
    paginator = Paginator(expenses,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # 'expenses': expenses,
        'total_expenses': round(total_expenses, 2),
        'monthly_budget': round(monthly_budget, 2),
        'remaining_budget': round(remaining_budget, 2),
        'expenses': page_obj,  # Pass paginated expenses
        'page_obj': page_obj,  # For pagination controls
    }

    return render(request, 'tracker/dashboard.html', context)


@login_required(login_url='/login/')
def add_expense(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_id_or_flag = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        paid_date = request.POST.get('paid_date')
        notes = request.POST.get('notes')

        # Determine category
        if category_id_or_flag == '__new__' and new_category_name:
            category_obj, _ = Category.objects.get_or_create(
                category=new_category_name.strip(),
                user=request.user
            )
        else:
            category_obj = get_object_or_404(Category, id=category_id_or_flag, user=request.user)

        # Create expense
        Expense.objects.create(
            user=request.user,
            title=title.strip(),
            amount=amount,
            category=category_obj,
            paid_date=paid_date,
            notes=notes.strip()
        )

        messages.success(request, "Expense added successfully!")
        return redirect('user_dashboard')

    # GET request: Show form with user's categories
    categories = Category.objects.filter(user=request.user).order_by('category')
    return render(request, 'tracker/add_expense.html', {
        'categories': categories
    })


@login_required(login_url='/login/')
def update_expense(request, exp_id):
    expense = get_object_or_404(Expense, pk=exp_id, user=request.user)
    user_categories = Category.objects.filter(user=request.user).order_by('category')

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        paid_date = request.POST.get('paid_date')
        notes = request.POST.get('notes')

        if category_name == '__new__' and new_category_name:
            category_obj, created = Category.objects.get_or_create(
                category=new_category_name.strip(),
                user=request.user
            )
            # if created:
            #     messages.success(request, f"New category '{new_category_name}' created.")
        else:
            category_obj = Category.objects.filter(
                category=category_name, user=request.user
            ).first()
            if not category_obj:
                category_obj = Category.objects.create(
                    category=category_name.strip(),
                    user=request.user
                )

        expense.title = title
        expense.amount = amount
        expense.category = category_obj
        expense.paid_date = paid_date
        expense.notes = notes
        expense.save()

        messages.success(request, "Expense updated successfully!")
        return redirect('user_dashboard')

    return render(request, 'tracker/update_expense.html', {
        'expense': expense,
        'categories': user_categories,
    })


@login_required(login_url='/login/')
def delete_expense(request, exp_id):
    expense = get_object_or_404(Expense, pk=exp_id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted successfully!")
    return redirect('user_dashboard')

@login_required(login_url='/login/')
def set_monthly_budget(request):
    user = request.user
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Get month name like "June"
    month_name = calendar.month_name[current_month]

    budget, created = MonthlyBudget.objects.get_or_create(
        user=user,
        year=current_year,
        month=current_month,
        defaults={'amount': 0}
    )

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Budget cannot be negative")
        except ValueError:
            messages.warning(request, "Please enter a valid positive number for budget.")
            return redirect('set_monthly_budget')

        budget.amount = amount
        budget.save()
        messages.success(request, f"Monthly budget set to ₹{amount} for {month_name} {current_year}.")
        return redirect('user_dashboard')

    context = {
        'budget': budget,
        'month': current_month,
        'month_name': month_name,
        'year': current_year,
    }
    return render(request, 'tracker/set_budget.html', context)

@login_required
def report_view(request):
    user = request.user
    today = now().date()
    filter_type = request.GET.get('filter_type', 'weekly')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Set default filter ranges
    if filter_type == 'monthly':
        start = today - timedelta(days=30)
        end = today
    elif filter_type == 'yearly':
        start = today.replace(month=1, day=1)
        end = today
    elif filter_type == 'custom':
        start = parse_date(start_date) if start_date else today - timedelta(days=7)
        end = parse_date(end_date) if end_date else today
        if not start or not end:
            start = today - timedelta(days=7)
            end = today
    else:  # Default: weekly
        start = today - timedelta(days=7)
        end = today

    # Filter user's expenses in the selected date range
    filtered_expenses = Expense.objects.filter(user=user, paid_date__range=(start, end))

    weekly_total = filtered_expenses.filter(paid_date__gte=today - timedelta(days=7)).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_total = filtered_expenses.filter(paid_date__gte=today - timedelta(days=30)).aggregate(Sum('amount'))['amount__sum'] or 0

    by_category = (
        filtered_expenses
        .values('category__category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    daily_series = (
        filtered_expenses
        .values('paid_date')
        .annotate(total=Sum('amount'))
        .order_by('paid_date')
    )

    recurring = (
        filtered_expenses
        .values('category__category')
        .annotate(count=Count('id'))
        .filter(count__gte=2)
        .order_by('-count')
    )

    return render(request, 'tracker/report.html', {
        'weekly_total': weekly_total,
        'monthly_total': monthly_total,
        'by_category': by_category,
        'daily_series': list(daily_series),
        'recurring': recurring,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
        'has_data': filtered_expenses.exists(),
    })

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'
    fields = "__all__"
    redirect_authenticated_user = True
   
    def get_success_url(self):
        return reverse_lazy('index')

class RegisterPage(FormView):
    template_name = 'myapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(*args, **kwargs)

@login_required
def index(request):
    if request.method == 'POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.instance.user = request.user
            expense.save()

    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(Sum('amount'))

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data1 = Expense.objects.filter(date__gt=last_year, user=request.user)
    yearly_sum = data1.aggregate(Sum("amount"))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data2 = Expense.objects.filter(date__gt=last_month, user=request.user)
    monthly_sum = data2.aggregate(Sum("amount"))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data3 = Expense.objects.filter(date__gt=last_week, user=request.user)
    weekly_sum = data3.aggregate(Sum("amount"))

    daily_sums = Expense.objects.filter(user=request.user).values('date').order_by('date').annotate(sum=Sum('amount'))

    categorical_sums = Expense.objects.filter(user=request.user).values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    return render(request,'myapp/index.html',{'expense_form':expense_form, 'expenses':expenses, 'total_expenses':total_expenses, 'yearly_sum':yearly_sum, 'monthly_sum':monthly_sum, 'weekly_sum':weekly_sum, 'daily_sums':daily_sums, 'categorical_sums':categorical_sums})

@login_required
def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method == 'POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,'myapp/edit.html',{'expense_form' : expense_form})

@login_required
def delete(request,id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
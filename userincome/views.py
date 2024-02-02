from django.shortcuts import render, redirect
from django.contrib import messages
from .models  import Source,UserIncome
from django.core.paginator import  Paginator
from userpreferences.models import UserPreference
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income= UserIncome.objects.filter(owner=request.user).order_by('-date')
    currency=UserPreference.objects.get(user=request.user).currency

    context={
        'income':income,
        'currency':currency
    }
    return render(request, 'income/index.html',context)
# add-income
@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context={
        'sources':sources,
        'values':request.POST
        }
    if request.method =="GET":
         return render(request,'income/add_income.html', context)

    if request.method =="POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'income/add_income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'income/add_income.html', context)
        
        UserIncome.objects.create(owner=request.user,amount=amount,description=description, date=date,source=source)

        messages.success(request,'Record Saved Successfully')
        return redirect('userincome:incomes')
    

@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income=UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context={
        'income': income,
        'values': income,
        'sources': sources,

    }
    if request.method=="GET":
        return render(request,'income/edit_income.html',context)
    if request.method=="POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'income/edit_income.html', context)
        
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'income/edit_income.html', context)
        income.amount = amount
        income.source = source
        income.date= date
        income.description = description
        income.save()
        messages.success(request,'Record Updated Successfully')
        return redirect('userincome:incomes')
    

def income_delete(request, id):
    income=UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record deleted Successfully')
    return redirect ('userincome:incomes')

from django.shortcuts import render, redirect
from .models import Category,Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from userpreferences.models import UserPreference
import datetime
import json
from django.http import JsonResponse,HttpResponse
import csv
import xlwt
# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile
# from django.db.models import Sum
# import os

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    page_number = request.GET.get('page')
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)
# add-expense

def add_expense(request):
    categories = Category.objects.all()
    context={
        'categories':categories,
        'values':request.POST
        }
    if request.method =="GET":
         return render(request,'expenses/add_expense.html', context)

    if request.method =="POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/add_expense.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/add_expense.html', context)
        
        Expense.objects.create(owner=request.user,amount=amount,description=description, date=date,category=category)

        messages.success(request,'Expense Saved Successfully')
        return redirect('expenses:expense')
    

def expense_edit(request, id):
    expense=Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'expense': expense,
        'values': expense,
        'categories': categories,

    }
    if request.method=="GET":
        return render(request,'expenses/expense_edit.html',context)
    if request.method=="POST":
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expenses/expense_edit.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'Description is required')
            return render(request,'expenses/expense_edit.html', context)
        
        expense.user = request.user
        expense.amount = amount
        expense.category = category
        expense.date= date
        expense.description = description
        expense.save()
        messages.success(request,'Expense Updated Successfully')
        return redirect('expenses:expense')
    

def expense_delete(request, id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted Successfully')
    return redirect ('expenses:expense')

def expense_category_summary(request):
    todays_date=datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses= Expense.objects.filter(owner=request.user,date__gte=six_months_ago,date__lte=todays_date)
    final_rep={

    }
    def get_category(expense):
        return expense.category
    category_list=list(set(map(get_category,expenses)))
    def get_expense_category_amount(category):
        amount = 0
        filter_by_category=expenses.objects.filter(category=category)

        for item in filter_by_category:
            amount+=item.amount
        return amount
    for x in expenses:
        for y in category_list:
            final_rep[y]=get_expense_category_amount()

    return JsonResponse({'expense_category_date':final_rep},safe=False)

def stats_View(request):
    return render(request,'expenses/expense_category_summary.html')

def export_csv(request):
    response = HttpResponse(content_type ='text/csv')
    response['Content-Disposition']= 'attachment ;filename=Expenses'+  str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses=Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')
    for expense in expenses:
        writer.writerow([expenses.amount,expenses.description,expenses.category,expenses.date])
    return response

def export_excel(request):
    response = HttpResponse(content_type ='application/ms-excel')
    response['Content-Disposition']= 'attachment ;filename=Expenses'+  str(datetime.datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Expenses')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Description','Category','Date']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)

    return response


# def export_pdf(request):
#     response = HttpResponse(content_type ='application/pdf')
#     response['Content-Disposition']= 'attachment ;filename=Expenses'+  str(datetime.datetime.now())+'.pdf'
#     response['Content-Transfer-Encoding']='binary'
#     html_string = render_to_string('expenses/pdf-output.html',{'expenses':[],'total':0})
#     html = HTML(string=html_string)
#     result=html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output=open(output.name,'rb')
#         response.write(output.read())
#     return response


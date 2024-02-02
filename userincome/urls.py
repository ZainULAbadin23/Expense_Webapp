from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name = 'userincome'
urlpatterns = [
    path('',views.index, name="incomes"),
    path('edit_income/<int:id>',views.income_edit,name="income_edit"),
    path('add_income/',views.add_income,name="add_income"),
    path('delete_income/<int:id>', views.income_delete, name="income_delete"),
    
]

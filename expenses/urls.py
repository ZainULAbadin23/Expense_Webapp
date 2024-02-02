from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name = 'expenses'
urlpatterns = [
    path('',views.index, name="expense"),
    path('edit_expense/<int:id>',views.expense_edit,name="expense_edit"),
    path('add_expense/',views.add_expense,name="add_expense"),
    path('delete_expense/<int:id>', views.expense_delete, name="expense_delete"),
    path('expense-category-summary',views.expense_category_summary,name="expense_category_summary"),
    path('stats',views.stats_View,name="stats"),
    path('export-csv',views.export_csv,name="export-csv"),
    path('export-excel',views.export_excel,name="export-excel"),
    # path('export-pdf',views.export_pdf,name="export-pdf")
    
]

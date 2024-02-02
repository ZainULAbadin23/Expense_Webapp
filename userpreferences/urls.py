from django.urls import  path
from . import views

app_name="userpreferences"
urlpatterns = [
    path('general', views.index, name="preference"),

]

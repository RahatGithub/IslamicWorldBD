from django.urls import path 
from .views import * 

app_name = 'AdminPanel'

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories'),
    path('resources/', ResourceView.as_view(), name='resources'),

]
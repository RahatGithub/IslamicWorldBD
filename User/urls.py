from django.urls import path 
from .views import * 

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('categories/', CategoryView.as_view(), name='category_view'),
    path('resources/', ResourceView.as_view(), name='resource_view')
]
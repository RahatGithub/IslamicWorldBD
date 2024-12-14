from django.urls import path 
from .views import * 

app_name = 'AdminPanel'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('add-category/', AddCategoryView.as_view(), name='add-category'),
    path('add-category/<int:parent_id>/', AddCategoryView.as_view(), name='add-category-with-parent'),

]
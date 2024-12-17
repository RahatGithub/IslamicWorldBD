from django.urls import path 
from .views import * 

app_name = 'AdminPanel'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # category related paths 
    path('category/add/', AddCategoryView.as_view(), name='add-category'),
    path('category/add/<int:parent_id>/', AddCategoryView.as_view(), name='add-category-with-parent'),
    path('category/edit/<int:category_id>/', EditCategoryView.as_view(), name='edit-category'),

    # resource related paths
    path('resource/add/', AddResourceView.as_view(), name='add-resource'),
    path('resource/add/<int:category_id>/', AddResourceView.as_view(), name='add-resource-with-category'),
    path('resource/edit/<int:resource_id>/', EditResourceView.as_view(), name='edit-resource'),

]
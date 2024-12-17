from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from AdminPanel.models import *

class Index(View):
    def get(self, request):
        return HttpResponse("User/index.html")
    

class CategoryView(View):
    def get(self, request):
        category_id = request.GET.get('id')
        # is_top_level = request.GET.get('is_top_level')

        if category_id:
            try:
                category = Category.objects.get(pk=category_id, is_active=True)
                if Resource.objects.filter(category=category): # if this category has any resource
                    return redirect(f"/resources?category_id={category_id}")
                else:  # else it has subcategories 
                    categories = Category.objects.filter(parent_category=category, is_active=True)
            except Category.DoesNotExist:
                return HttpResponseNotFound("Category not found")
        else: 
            categories = Category.objects.filter(parent_category__isnull=True)

        return render(request, "User/categories.html", {'categories':categories})
    

class ResourceView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        
        if category_id:
            try:
                category = Category.objects.get(pk=category_id, is_active=True)
                resources = Resource.objects.filter(category=category, is_active=True)
            except Category.DoesNotExist:
                return HttpResponseNotFound("Resource not found")
        else:
            resources = Resource.objects.all()
        return render(request, "User/resources.html", {'resources':resources})
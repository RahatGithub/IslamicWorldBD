from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from AdminPanel.models import *

class Index(View):
    def build_hierarchy(self, category):
        """
        Recursively build a hierarchical structure for a given category.
        """
        subcategories = Category.objects.filter(parent_category=category, is_active=True)

        if subcategories.exists():
            return {
                "id": category.id,
                "name": category.name,
                "subcategories": [self.build_hierarchy(sub) for sub in subcategories],
            }
        else:
            resources = Resource.objects.filter(category=category, is_active=True)
            return {
                "id": category.id,
                "name": category.name,
                "resources": [
                    {"id": res.id, "name": res.name, "link": res.link, "description": res.description, "is_recommended": res.is_recommended}
                    for res in resources
                ],
            }

    def get_hierarchy(self):
        """
        Build the entire hierarchy starting from root categories.
        """
        root_categories = Category.objects.filter(parent_category=None, is_active=True)
        return [self.build_hierarchy(root) for root in root_categories]


    def get(self, request):
        # Build the hierarchy
        hierarchy = self.get_hierarchy()

        # Fetch all categories 
        categories = Category.objects.filter(parent_category__isnull=True, is_active=True)

        # Pass the hierarchy to the template
        return render(request, "User/index.html", {"categories": categories, "hierarchy": hierarchy})
    

class CategoryView(View):
    def get(self, request):
        category_id = request.GET.get('id')

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
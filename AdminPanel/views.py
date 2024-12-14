from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from .models import *


class CategoryView(View):
    def build_hierarchy(self, category):
        """
        Recursively build a hierarchical structure for a given category.
        """
        subcategories = Category.objects.filter(parent_category=category, is_active=True)

        if subcategories.exists():
            return {
                "name": category.name,
                "subcategories": [self.build_hierarchy(sub) for sub in subcategories],
            }
        else:
            resources = Resource.objects.filter(category=category, is_active=True)
            return {
                "name": category.name,
                "resources": [{"name": res.name, "link": res.link, "description": res.description} for res in resources],
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
        # Pass the hierarchy to the template
        return render(request, "AdminPanel/categories.html", {"hierarchy": hierarchy})

    

class ResourceView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        
        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
                resources = Resource.objects.filter(category=category)
            except Exception:
                raise models.exceptions.ValidationError(f"Category with ID {category_id} does not exist.") 
        else:
            resources = Resource.objects.all()
        return render(request, "AdminPanel/resources.html", {'resources':resources})
        # return HttpResponse(f"resources of the category: {category_id}")
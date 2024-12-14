from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from .models import *
from .forms import CategoryForm

class DashboardView(View):
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
                "resources": [{"id": res.id,"name": res.name, "link": res.link, "description": res.description} for res in resources],
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
        return render(request, "AdminPanel/dashboard.html", {"hierarchy": hierarchy, "is_first_render": True})




class AddCategoryView(FormView):
    template_name = 'AdminPanel/add_category.html'
    form_class = CategoryForm

    def get_initial(self):
        """Set the initial data for the form."""
        initial = super().get_initial()
        parent_id = self.kwargs.get('parent_id')  # Get parent_id from URL
        if parent_id:
            parent_category = get_object_or_404(Category, id=parent_id)
            initial['parent_category'] = parent_category.id  # Set initial value for parent_category
        return initial

    def form_valid(self, form):
        """Save the form and redirect to success."""
        form.save()
        return redirect('/adminPanel/dashboard/') 

    def get_context_data(self, **kwargs):
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        parent_id = self.kwargs.get('parent_id')
        if parent_id:
            context['parent_category'] = get_object_or_404(Category, id=parent_id)
        else:
            context['parent_category'] = None
        return context
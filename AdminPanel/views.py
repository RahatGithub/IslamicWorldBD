from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/adminPanel/dashboard') 


class DashboardView(LoginRequiredMixin, View):
    login_url = '/auth/login/'  # Redirect to the login URL if not logged in

    def build_hierarchy(self, category):
        """
        Recursively build a hierarchical structure for a given category.
        """
        subcategories = Category.objects.filter(parent_category=category)

        if subcategories.exists():
            return {
                "id": category.id,
                "name": category.name,
                "is_active": category.is_active,
                "subcategories": [self.build_hierarchy(sub) for sub in subcategories],
            }
        else:
            resources = Resource.objects.filter(category=category)
            return {
                "id": category.id,
                "name": category.name,
                "is_active": category.is_active,
                "resources": [
                    {"id": res.id, "name": res.name, "link": res.link, "description": res.description, "is_active": res.is_active, "is_recommended": res.is_recommended}
                    for res in resources
                ],
            }

    def get_hierarchy(self):
        """
        Build the entire hierarchy starting from root categories.
        """
        root_categories = Category.objects.filter(parent_category=None)
        return [self.build_hierarchy(root) for root in root_categories]

    def dispatch(self, request, *args, **kwargs):
        """
        Ensure the user is authenticated and has superuser permissions.
        """
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        if not request.user.is_superuser:
            return redirect(self.login_url)  # Redirect non-superusers to login
        return super().dispatch(request, *args, **kwargs)

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



class EditCategoryView(FormView):
    template_name = 'AdminPanel/edit_category.html'
    form_class = EditCategoryForm

    def get_success_url(self):
        # Redirect to the dashboard
        return reverse_lazy('AdminPanel:dashboard')

    def get_form(self, *args, **kwargs):
        # Fetch the category instance based on the URL parameter
        self.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return self.form_class(instance=self.category, **self.get_form_kwargs())

    def form_valid(self, form):
        # Save the updated category instance
        form.save()
        return super().form_valid(form)



class AddResourceView(FormView):
    template_name = 'AdminPanel/add_resource.html'
    form_class = ResourceForm

    def get_initial(self):
        """Set the initial data for the form."""
        initial = super().get_initial()
        category_id = self.kwargs.get('category_id')  
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            initial['category'] = category.id  
        return initial

    def form_valid(self, form):
        """Save the form and redirect to success."""
        form.save()
        return redirect('/adminPanel/dashboard/') 

    def get_context_data(self, **kwargs):
        """Add extra context data to the template."""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        if category_id:
            context['category'] = get_object_or_404(Category, id=category_id)
        else:
            context['category'] = None
        return context
    

class EditResourceView(FormView):
    template_name = 'AdminPanel/edit_resource.html'
    form_class = EditResourceForm

    def get_success_url(self):
        # Redirect to the dashboard
        return reverse_lazy('AdminPanel:dashboard')

    def get_form(self, *args, **kwargs):
        # Fetch the category instance based on the URL parameter
        self.resource = get_object_or_404(Resource, pk=self.kwargs['resource_id'])
        return self.form_class(instance=self.resource, **self.get_form_kwargs())

    def form_valid(self, form):
        # Save the updated category instance
        form.save()
        return super().form_valid(form)
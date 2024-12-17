from django import forms
from .models import Category, Resource

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent_category', 'image', 'is_active']
        widgets = {
            'parent_category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, parent_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if parent_id:
            self.fields['parent_category'].initial = parent_id
        else:
            self.fields['parent_category'].initial = None


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent_category', 'image', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['category', 'name', 'link', 'image', 'description', 'author', 'is_recommended', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, category_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if category_id:
            self.fields['category'].initial = category_id
        else:
            self.fields['category'].initial = None


class EditResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['category', 'name', 'link', 'image', 'description', 'author', 'is_recommended', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_recommended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
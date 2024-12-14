from django import forms
from .models import Category

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
from django.contrib import admin
from .models import Category, Resource

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category', 'is_active', 'order')
    list_filter = ('is_active', 'parent_category')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'is_active', 'is_recommended', 'order')
    list_filter = ('is_active', 'is_recommended', 'category')
    search_fields = ('name', 'author', 'description')
    ordering = ('id',)

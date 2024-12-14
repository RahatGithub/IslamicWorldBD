from django.db import models

# class Category(models.Model):
#     name = models.CharField(max_length=300)
#     parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='category_images/', blank=True)
#     order = models.PositiveSmallIntegerField(default=0, blank=True)
#     is_active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return f"{self.id}. {self.name}"
    

from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=300)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/', blank=True)
    order = models.PositiveSmallIntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True)
    
    def clean(self):
        # Prevent a category from being its own parent
        if self.parent_category == self:
            raise ValidationError("A category cannot be its own parent.")
        
        # Check for indirect circular references
        ancestor = self.parent_category
        while ancestor is not None:
            if ancestor == self:
                raise ValidationError("Circular reference detected in the category hierarchy.")
            ancestor = ancestor.parent_category

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}. {self.name}"




class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to='resource_images/', blank=True)
    description = models.TextField(blank=True) 
    author = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True) 
    is_recommended = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

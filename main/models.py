from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=300)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    # order = models.PositiveSmallIntegerField(default=0, blank=True)
    
    def __str__(self):
        return f"{self.id}. {self.name}"



class Resource(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField()
    image = models.ImageField(upload_to='resource_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # order = models.PositiveSmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.name
from rest_framework import viewsets
from .models import Resource, Category
from .serializers import ResourceSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError



class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        parent_category_id = request.GET.get('id')
        if parent_category_id:
            try:
                parent_category = Category.objects.get(pk=parent_category_id)
                queryset = self.queryset.filter(parent_category=parent_category)
            except Category.DoesNotExist:
                raise ValidationError(f"Category with ID {parent_category_id} does not exist.")
        else:
            queryset = self.queryset.filter(parent_category__isnull=True)  # Top-level categories

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    is_delete = serializers.BooleanField(read_only=True)
    is_available = serializers.BooleanField(required=False)
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'shop', 'location', 
            'price', 'discount', 'category', 'stock', 'is_available', 
            'picture', 'is_delete', '_links'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is available'] = representation.get('is_available')
        representation[' _links'] = representation.get('_links')
        representation['is delete'] = representation.get('is_delete')
        
        return representation

    def get__links(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/products') if request else 'http://localhost:8000/products'
        
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        return [
            {
                "rel": "self",
                "href": f"{base_url}",
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"{base_url}/{obj.id}/",
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"{base_url}/{obj.id}/",
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"{base_url}/{obj.id}/",
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]
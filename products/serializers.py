from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get__links(self, obj):
        return [
            {
                "rel": "self",
                "href": "/products",
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"/products/{obj.id}/",
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"/products/{obj.id}/",
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": f"/products/{obj.id}/",
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
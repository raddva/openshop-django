from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(APIView):
    def get(self, request):
        name_query = request.query_params.get('name', None)
        location_query = request.query_params.get('location', None)
        queryset = Product.active_objects.all()
        
        if name_query is not None:
            queryset = queryset.filter(name__icontains=name_query)
            
        if location_query is not None:
            queryset = queryset.filter(location__icontains=location_query)

        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        if 'is available' in data and 'is_available' not in data:
            data['is_available'] = data['is_available']

        serializer = ProductSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailUpdateDeleteAPIView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except (Product.DoesNotExist, ValueError):
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        product.is_delete = True
        product.save()
        return Response(
            {"message": "data has been deleted"}, 
            status=status.HTTP_200_OK
        )
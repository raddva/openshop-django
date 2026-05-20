from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(APIView):

    def get(self, request):

        name = request.query_params.get('name')
        location = request.query_params.get('location')

        products = Product.objects.all()

        if name:
            products = products.filter(name__icontains=name)

        if location:
            products = products.filter(location__icontains=location)

        serializer = ProductSerializer(products, many=True)

        return Response({
            "products": serializer.data
        })

    def post(self, request):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    def put(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        product = self.get_object(pk)

        if not product:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Soft delete
        product.is_delete = True
        product.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
from django.shortcuts import render
from product.models import Beer,Order
from product.serializers import BeerSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404



class BeerList(APIView):
    def get(self,request):
            beer = Beer.objects.all()
            serializer = BeerSerializer(beer,many=True,context={'request': request})
            return Response(serializer.data)
    def post(self, request):
        serializer = BeerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BeerDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Beer.objects.get(pk=pk)
        except Beer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        beer = self.get_object(pk)
        serializer = BeerSerializer(beer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        beer = self.get_object(pk)
        serializer = BeerSerializer(beer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        beer = self.get_object(pk)
        beer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    def get(self,request):
            order = Order.objects.all()
            serializer = OrderSerializer(order,many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
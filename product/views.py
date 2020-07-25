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
        return Response('successful',status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    def get(self,request):
            order = Order.objects.all()
            serializer = OrderSerializer(order,many=True)
            return Response(serializer.data)
    def post(self, request):
        try:
            for data in request.data:
                product_input = data.get('product')
                print(product_input)

                user = request.user
                product = product_input.get('id')
                print(product)
                price = product_input.get('price')
                number = data.get('quantity')
                money = float(price) * int(number)
                order = Order.objects.create(
                    user = user,
                    product_id = product,
                    money = money, 
                    number = number,
                )
                order.save()
            return Response("successful", status=status.HTTP_201_CREATED)
        except:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response('successful',status=status.HTTP_204_NO_CONTENT)
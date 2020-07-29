from django.shortcuts import render
from product.models import Product,Order,Category
from product.serializers import ProductSerializer,OrderSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from apyori import apriori
from pandas import DataFrame    



class ProductList(APIView):
    def get(self,request):
            product = Product.objects.all()
            serializer = ProductSerializer(product,many=True,context={'request': request})
            return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print(pk)
        product = self.get_object(pk)
        print(product)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response('successful',status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    def get(self,request):
            order = Order.objects.all()
            serializer = OrderSerializer(order,many=True)
            return Response(serializer.data)
    def post(self, request):
        # try:
            count_order  = Order.objects.all()
            for data in request.data:
                product_input = data.get('product')
                user = request.user
                product = product_input.get('id')
                price = product_input.get('price')
                number = data.get('quantity')
                money = float(price) * int(number)
                order = Order.objects.create(
                    user = user,
                    product_id = product,
                    money = money, 
                    number = number,
                    iteam_code = len(count_order)+1,
                )
                order.save()
            return Response("successful", status=status.HTTP_201_CREATED)
        # except:
        #     return Response("error", status=status.HTTP_400_BAD_REQUEST)

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


class Apriori(APIView):
    def post(self, request):
        result=[]
        list_order = Order.objects.all().distinct('iteam_code')
        list_iteam_code =[]
        for i in list_order:
            list_iteam_code.append(i.iteam_code)
        transactions = []
        for x in list_iteam_code:
            orders = Order.objects.filter(iteam_code = x).distinct('product__category_id')
            items = [] 
            for order in orders:
                items.append(order.product.category_id)
            transactions.append(items)
        results = list(apriori(transactions))
        array1 = []
        array2 = []
        array3 = []
        category = Category.objects.all()
        result=[]
        input = request.data.get('product')
        for RelationRecord in results:
            t3 = {}
            for ordered_stat in RelationRecord.ordered_statistics:
                if len(input)>0:
                    if list(ordered_stat.items_base) == input:
                        t3['items_add'] =list(ordered_stat.items_add)
                        t3['confidence'] = ordered_stat.confidence
                        result.append(t3)
                else:
                    return Response(None)
        print(result)
                # Support.append(RelationRecord.support)
                # Items.append(RelationRecord.items)
                # Antecedent.append(ordered_stat.items_base)
                # Consequent.append(ordered_stat.items_add)
                # Confidence.append(ordered_stat.confidence)
                # Lift.append(ordered_stat.lift)
        #         if len(RelationRecord.items)==2:
        #             if len(ordered_stat.items_base)==1:
        #                 x = list(ordered_stat.items_base)
                        
        #                 a['items'] = list(RelationRecord.items)
        #                 a['items_base'] = x
        #                 a['items_add'] = list(ordered_stat.items_add)
        #                 a['confidence'] = ordered_stat.confidence
        #                 a['lift'] = ordered_stat.lift
        #                 a['support'] = RelationRecord.support
        #                 array1.append(a)
        #         if len(RelationRecord.items)==3:
        #             if len(ordered_stat.items_base)==1:
        #                 c['items'] = list(RelationRecord.items)
        #                 x = list(ordered_stat.items_base)
        #                 c['items_base'] = x
        #                 c['items_add'] = list(ordered_stat.items_add)
        #                 c['confidence'] = ordered_stat.confidence
        #                 c['lift'] = ordered_stat.lift
        #                 c['support'] = RelationRecord.support
        #                 array2.append(c)
        #             if len(ordered_stat.items_base)==2:
                    
        #                 b['items'] = list(RelationRecord.items)
        #                 b['items_base'] =list(ordered_stat.items_base)
        #                 b['items_add'] = list(ordered_stat.items_add)
        #                 b['confidence'] = ordered_stat.confidence
        #                 b['lift'] = ordered_stat.lift
        #                 b['support'] = RelationRecord.support
        #                 array3.append(b)

        # result=[]
        # input = [3,1]
        # print(array3)
        # for a in array1:
        #     t1 = {}
        #     if a.get('items_base') == input:
        #         t1['items_add'] = a.get('items_add')
        #         t1['confidence'] = a.get('confidence')
        #         result.append(t1)
        # for b in array2: 
        #     t2 = {}
        #     if b.get('items_base') == input:
        #         t2['items_add'] = b.get('items_add')
        #         t2['confidence'] = b.get('confidence')
        #         result.append(t2)
            
        # for c in array3:
        #     t3 = {}
        #     if c.get('items_base') == input or c.get('items_base') == [1,3]:
        #         t3['items_add'] = c.get('items_add')
        #         t3['confidence'] = c.get('confidence')
        #         result.append(t3)
        # print(result)
        index = 0
        if len(result)>0:
            check = result[0].get('confidence')
            for i,y in enumerate(result):
                if check < y.get('confidence'):
                    check = y.get('confidence')
                    index = i
            kq  = result[index].get('items_add')
            print(kq)

            product = Product.objects.filter(category_id__in = kq)
            productSerializer = ProductSerializer(product,many=True,context={'request': request})

        return Response(productSerializer.data)
        

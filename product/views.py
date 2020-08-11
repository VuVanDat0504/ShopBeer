from django.shortcuts import render
from product.models import Product,Order,Category
from product.serializers import ProductSerializer,OrderSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from apyori import apriori
from pandas import DataFrame    


class CategoryList(APIView):
    def get(self,request):
        queryset =  Category.objects.all()
        category = CategorySerializer(queryset,many= True)
        return Response(category.data)


class ProductList(APIView):
    def get(self,request):
            category_id =request.GET.get('category_id')
            if category_id is not None:
                product = Product.objects.filter(category_id = category_id)
            else:
                product = Product.objects.filter()
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
            count_order  = Order.objects.all().distinct('iteam_code').count() + 1
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
                    iteam_code = '10' + str(count_order).zfill(4),
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
        print(transactions)
        
        print(results)
        category = Category.objects.all()
        result=[]
        input = request.data.get('product')
        input.sort()
        print(input)
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
        index = 0
        if len(result)>0:
            check = result[0].get('confidence')
            for i,y in enumerate(result):
                if check < y.get('confidence'):
                    check = y.get('confidence')
                    index = i
            # ??loi
            kq  = result[index].get('items_add')
            print(kq)
            product = Product.objects.filter(category_id__in = kq)
            productSerializer = ProductSerializer(product,many=True,context={'request': request})
        #print 
        df = DataFrame(columns=('Items','Antecedent','Consequent','Support','Confidence','Lift'))

        Support =[]
        Confidence = []
        Lift = []
        Items = []
        Antecedent = []
        Consequent=[]

        for RelationRecord in results:
            for ordered_stat in RelationRecord.ordered_statistics:
                Support.append(RelationRecord.support)
                Items.append(RelationRecord.items)
                Antecedent.append(ordered_stat.items_base)
                Consequent.append(ordered_stat.items_add)
                Confidence.append(ordered_stat.confidence)
                Lift.append(ordered_stat.lift)

        df['Items'] = list(map(set, Items))                                   
        df['Antecedent'] = list(map(set, Antecedent))
        df['Consequent'] = list(map(set, Consequent))
        df['Support'] = Support
        df['Confidence'] = Confidence
        df['Lift']= Lift
        print(df)

        return Response(productSerializer.data)
        

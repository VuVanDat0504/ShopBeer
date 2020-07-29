from django.shortcuts import render
from user.models import MyUser
from user.serializers  import MyUserSerializer,TokenSerializer,CurrentUserSerializer,UserSerializer,GetMyUserSerializer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.models import Permission
from django.http import Http404
from rest_framework import generics

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializer


class UserProfile(APIView):
    def get(self,request):
        user = MyUser.objects.get(user_id = request.user.id)
        userSerializer = GetMyUserSerializer(user)
        return Response(userSerializer.data)

class MyUsers(APIView):
    def get(self,request):
        user = MyUser.objects.all()
        serializer = GetMyUserSerializer(user,many=True)
        return Response(serializer.data)
        
    def post(self, request):
        try:
            userSerializer = UserSerializer(data=request.data)
            userSerializer.is_valid(raise_exception=True)
            user = userSerializer.save()
            myUserSerializer = MyUserSerializer(data={
                **request.data,
                'user_id': user.id
            })
            myUserSerializer.is_valid(raise_exception=True)

            myUser = myUserSerializer.save()
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(err.args, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
   
    def get_object(self, pk):
        try:
            return MyUser.objects.get(user_id=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = MyUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        try:
        
            user = self.get_object(pk)
            username =request.data.get('username')
            first_name =request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            is_superuser =  request.data.get('is_superuser')
            password = request.data.get('password')

            if password != '':
                user.set_password(password)
        
            serializer = MyUserSerializer(user, data={'username':username,'first_name':first_name,'last_name':last_name,'email':email,'is_superuser':is_superuser},partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(err.args, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = MyUser.objects.get(user_id = pk)
        user.delete()
        return Response('succesful',status=status.HTTP_204_NO_CONTENT)

class ChangePassword(APIView):
    def post(self,request):
      try:
        password =request.data.get('password')
        new_password = request.data.get('new_password')  

        if password == new_password:
          return Response("The new password has already been used",status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if  user.check_password(password):
            user.set_password(new_password)
            user.save()
            return Response("Password has been changed",status=status.HTTP_200_OK)
        else:
          return Response("Password incorrect",status=status.HTTP_400_BAD_REQUEST) 
      except Exception as err:
        return Response(err.args, status=status.HTTP_400_BAD_REQUEST)

class test(generics.GenericAPIView):
    def post(self, request):
        store_data = pd.read_csv('D:\\Datasets\\test.csv',header=None, error_bad_lines=False)
        # store_data = pd.read_csv('D:\\Datasets\\csv_result-storiescsv', header=None)
        store_data.head()
        print(store_data.head())
        print(len(store_data),"okkkkkkkkkkkk")
        records = []
        for i in range(0, 218):
            records.append([str(store_data.values[i,j]) for j in range(0, 5)])
        association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=3)
        association_results = list(association_rules)
        # print(len(association_results))
        print(len(association_results))
        # print(association_results[0])
        for item in association_results:

            # first index of the inner list
            # Contains base item and add item
            pair = item[0] 
            items = [x for x in pair]
            print("Rule: " + items[0] + " -> " + items[1])

            #second index of the inner list
            print("Support: " + str(item[1]))

            #third index of the list located at 0th
            #of the third index of the inner list

            print("Confidence: " + str(item[2][0][2]))
            print("Lift: " + str(item[2][0][3]))
            print("=====================================")
        # return Response(association_results[0])
        return Response("okoko")


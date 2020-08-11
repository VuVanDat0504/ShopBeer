
from django.urls import path
from product.views import ProductDetail, ProductList,OrderList,OrderDetail,Apriori,CategoryList

urlpatterns = [
    path('beers/', ProductList.as_view()),
    path('beers/<int:pk>/', ProductDetail.as_view()),
    path('order/', OrderList.as_view()),
    path('order/<int:pk>/', OrderDetail.as_view()),
    path('apriori/', Apriori.as_view()),
    path('category/',CategoryList.as_view()),



]
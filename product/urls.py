
from django.urls import path
from product.views import BeerDetail, BeerList,OrderList,OrderDetail

urlpatterns = [
    path('beers/', BeerList.as_view()),
    path('beers/<int:pk>/', BeerDetail.as_view()),
    path('order/', OrderList.as_view()),
    path('order/<int:pk>/', OrderDetail.as_view()),


]
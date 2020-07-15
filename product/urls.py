
from django.urls import path
from product.views import BeerDetail, BeerList,OrderList

urlpatterns = [
    path('beers/', BeerList.as_view()),
    path('beers/<int:pk>/', BeerDetail.as_view()),
    path('order/', OrderList.as_view()),

]
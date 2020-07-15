from rest_framework import serializers
from product.models import Beer,Order

class BeerSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = Beer
        fields ='__all__'
  
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__'
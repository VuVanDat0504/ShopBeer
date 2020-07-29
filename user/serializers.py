from rest_framework import serializers
from user.models import MyUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class MyUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = MyUser
        fields = (
            'id',
            'gender',
            'age',
            'user_id',
        )
class GetMyUserSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    is_superuser = serializers.ReadOnlyField(source='user.is_superuser')

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name','gender','age','is_superuser')



class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # print('attrs self: ', attrs[self.username_field])
        data =  super(TokenSerializer, self).validate(attrs)
        data.update({'is_superuser': self.user.is_superuser})
        data.update({'username': self.user.username })

        return data
class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','is_superuser','first_name','last_name']

  

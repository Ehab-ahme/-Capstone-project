from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model= Category
        fields=  "__all__" #['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta():
        model= MenuItem
        fields= ['id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):
    user= serializers.PrimaryKeyRelatedField(
        queryset= User.objects.all(),
        default= serializers.CurrentUserDefault
    )
    def validate(self, attrs):
        attrs['price']= attrs['unit_price'] * attrs['quantity']
        return attrs
    
    class Meta():
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        extra_kwargs= {
            "price": {'read_only': True},
        }

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta():
        model= OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    orderitem= OrderItemSerializer(read_only=True, many= True, source='order')
    # we rename it to orderitem in the serializer to clearly indicate it holds the order’s items, not the order itself. 
    class Meta():
        model= Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class UserSerializer(serializers.ModelSerializer):
    model= User
    fields= ['id', 'username', 'email']
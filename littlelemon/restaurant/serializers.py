from rest_framework import serializers
from django.contrib.auth.models import User
from.models import MenuItems, Booking

class UserSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = User
        fields =  ['url', 'username', 'email', 'groups']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItems
        fields =  '__all__'   #['id', 'title', 'price', 'inventory']
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta():
        model= Booking
        fields = '__all__'
from rest_framework import generics, viewsets, status
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.response import Response



class CategoryView(generics.ListCreateAPIView):
    queryset= Category.objects.all()
    serializer_class= CategorySerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes= [IsAuthenticated]
        return [permission() for permission in permission_classes]

class MenuItemView(generics.ListCreateAPIView):
    queryset= MenuItem.objects.all()
    serializer_class= MenuItemSerializer
    search_fields = ['category__title']
    ordering_fields = ['price', 'inventory']
    
    def get_permissions(self):
        permission_classes= []
        if self.request.method != 'GET':
            permission_classes= [IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.all().filter(user= self.request.user)
    
    def delete(self, request, *args,**kwargs):
        Cart.objects.all().filter(user= self.request.user).delete()
        return Response('ok')

class OrderView(generics.ListCreateAPIView):
    queryset= Order.objects.all()
    serializer_class= OrderSerializer
    parser_classes= [IsAuthenticated]
    def get_queryset(self):
        user= self.request.user
        # If the user doesn't belong to any group.
        if user.groups.count() ==0: 
            return Order.objects.all().filter(user = user)
        # If the user belong to Delivery crew group.
        elif user.groups.filter(name = 'Delivery crew').exists():
            return Order.objects.all().filter(delivery_crew= user)
        # The other sttaf (Admin, managers)
        else:
            return Order.objects.all()
    #Create a new order when a user sends a request.
    def create(self, request, *args, **kwargs):
        user= self.request.user
        #Counting how many items belong to the user in the cart
        menuitem_count= Cart.objects.all().filter(user= user).count()
        if menuitem_count == 0 : #Meaning the cart is empty
            return Response ({"message:": "no item in the cart"})
        #(request.data) is Immutable= unchangable If you try, you'll get an error, so we'll take a copy.
        data= request.data.copy()
        #Then calculate the total price, And add it with it's ID in his request to get 'A safe request'.
        total= self.request.get_total_price(user)
        data['total']= total
        data['user']= user.id
        order_serializer= OrderSerializer(data=data)
        if order_serializer.is_valid():
            order= order_serializer.save()
        
        items= Cart.objects.all().filter(user= user)
        for item in items.values():
            orderitem= OrderItem(
                order= order, 
                menuitem_id= item['menuitem_id'],
                quantity= item['quantity'],
                price= item['price'],
            )
            orderitem.save()
        
        Cart.objects.all().filter(user=user).delete()
        
        result= order_serializer.data.copy()
        result['total']= total
        return Response(order_serializer.data)
    
    def get_total_price(self, user):
        total= 0
        items = Cart.objects.all().filter(user= user)
        for item in items.values():
            total += item['price']
        return total

class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset= Order.objects.all()
    serializer_class= OrderSerializer
    permission_classes= [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: # Normal user, not belonging to any group = Customer
            return Response('Not Ok')
        else: #everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)

# This defines a view set class that groups related views for managing user groups, specifically the "Manager" group.
class GroupViewSets(viewsets.ViewSet):
    permission_classes= [IsAdminUser]
    def list(self, request): # fetch Managers from the DB, so must use serializers
        users= User.objects.all().filter(groups__name='Manager') # two underscores it’s a way to look "through" relationships between database tables. See Explaination.md 37
        serialized_users= UserSerializer(users, many= True)
        return Response(serialized_users.data)
    
    def create(self, request):
        user= get_object_or_404(User, username= request.data['username'])
        managers= Group.objects.get(name= 'Managers')
        managers.user_set.add(user)
        return Response({'message':'user added to the managers group'}, 200)
    
    def destroy(self, request):
        user= get_object_or_404(User, username= request.data['username'])
        managers= Group.objects.get(name= 'Managers')
        managers.user_set.remove(user)
        return Response({'message':'user removed from the managers group'}, 200)
    
class DeliveryCrewViewsets(viewsets.ViewSet):
    permission_classes= [IsAuthenticated]
    def list(self, request): #For all users
        user= User.objects.all().filter(groups__name= "Delivery crew")
        items= UserSerializer(user, many= True)
        return Response(items.data)
    
    def create(self, request):
        #Only for managers
        if self.request.user.is_superuser ==False:
            if self.request.user.groups.filter(name="Managers").exists() == False:
                return Response({"message": "forbidden"}, status.HTTP_403_FORBIDDEN)
        user= get_object_or_404(User, request.data['username'])
        dc= Group.objects.get(name= "Delivery crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"})
    
    def destroy(self, request):
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name= "Managers").exists() == False:
                return Response({"message": "forbidden"}, status.HTTP_403_FORBIDDEN)
        user= get_object_or_404(User, request.data['username'])
        dc= Group.objects.get(name= 'Delivery crew')
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"})
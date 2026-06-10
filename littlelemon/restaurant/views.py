from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from.models import MenuItems, Booking
from.serializers import MenuItemSerializer, BookingSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

class MenuItemsView(generics.ListCreateAPIView):
    queryset= MenuItems.objects.all()
    serializer_class= MenuItemSerializer

class SingleMenuItemsView(generics.RetrieveUpdateDestroyAPIView):
    queryset= MenuItems.objects.all()
    serializer_class= MenuItemSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset= Booking.objects.all()
    serializer_class= BookingSerializer
    permission_classes= [IsAuthenticated]
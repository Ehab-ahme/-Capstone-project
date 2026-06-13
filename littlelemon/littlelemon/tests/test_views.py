from django.test import TestCase
from restaurant.views import MenuItemsView, MenuItemSerializer
from restaurant.models import MenuItems

class MenuViewTest(TestCase):
    
    def setUp(self):
        #1- إنشاء عناصر تجريبية في قاعدة البيانات المؤقتة
        MenuItems.objects.create(title= "Cake", price= 8, inventory= 10)
        MenuItems.objects.create(title= "Pizza", price= 12.99, inventory= 5)
        #2- إرسال طلب GET باستخدام self.client
    def test_getall(self):
        response= self.client.get('/restaurant/menu-items/')
        #3-serializer by JSON جلب البيانات من قاعدة البيانات وتحويلها لـ
        menu_items = MenuItems.objects.all()
        menu_serializer= MenuItemSerializer(menu_items, many= True)
        #4-Make a comparason between The response and serializer
        self.assertEqual(response.data, menu_serializer.data)
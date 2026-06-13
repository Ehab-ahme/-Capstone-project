from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.index, name= 'index'),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemsView.as_view()),
    # path('api-token-auth/', obtain_auth_token),
]
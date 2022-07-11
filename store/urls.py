from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout,name='logout'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.CheckOut.as_view(),name='Checkout'),

]
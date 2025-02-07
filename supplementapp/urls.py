from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import *


app_name = "supplementapp"


router = DefaultRouter()
router.register(r'status', Productviewset)

urlpatterns = [
    path('',views.home, name='home'),
    path('api/', include(router.urls)),
    path('product',views.Product , name = 'product'),
    path('aboutus',views.Aboutus , name = 'aboutus'),
    path('contactus',views.Contactus , name = 'contactus'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('login',views.Login , name = 'login'),
    path('register',views.Register , name = 'register'),
    path('logout',views.Logout , name = 'logout'),
    path('basket', views.view_basket, name='basket'),
    path('add-to-basket/<int:pk>',views.Add_to_basket , name = 'add-to-basket'),
    path('remove_from_basket/<int:pk>/', views.remove_from_basket, name='remove_from_basket'),
    path('checkout', views.Checkout, name='checkout'),
    path('payment_success', views.Payment_success, name='payment_success'),
    path('orders/', orders, name='orders'),
    path('profile/', profile, name='profile'),


]

if settings.DEBUG:  # فقط در حالت دیباگ
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

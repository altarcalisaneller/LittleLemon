"""littlelemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path, include  
from rest_framework import routers
from restaurant import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

router.register(r'booking', views.BookingViewSet)
# router.register(r'menu', views.MenuViewSet)


urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)),
    path('api/menu/', views.MenuItemView.as_view(), name="menu"), # DefaultRouter yalnızca viewsets.ModelViewSet tabanlı görünümleri destekler. O nedenle yukarda register edemiyorum ve dolayısıyla root da göremiyorum.
    path('api/menu/<int:pk>', views.SingleMenuItemView.as_view()),
    #path('api/users/', views.users), # djoser kullandığım için gerek kalmadı
    #path('api-token-auth/', obtain_auth_token), # djoser kullandığım için gerek kalmadı.obtain_auth_token bir görünüm fonksiyonunu temsil eder. Bu fonksiyon, kullanıcı adı ve şifre ile token almak için kullanılır. api-token-auth/ yoluna yapılan POST isteğiyle birlikte kullanıcı adı ve şifre gönderilir ve bu fonksiyon kullanıcıyı doğrularak bir token döndürür.
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('restaurant.urls')),
]
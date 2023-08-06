from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
#from rest_framework.decorators import api_view, permission_classes
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
import json
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer #, UserSerializer
#from .forms import BookingForm

# Create your views here.

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings) # Burada 'json' argümanı, veriyi JSON formatında bir metin dizesine (string) dönüştüreceğini belirtir.
    return render(request, 'bookings.html',{"bookings":booking_json})


def book(request):
    # form = BookingForm() # JS kullandım. O nedenle form kullanmadım.
    # if request.method == 'POST':
    #     form = BookingForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # context = {'form':form}
    return render(request, 'book.html', {})


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 


@csrf_exempt # crsf kontrolü yapmasını istemedim.
def bookings(request):
    if request.method == 'POST':
        data = json.load(request) # json.load() işlevi, JSON formatında yazılmış bir veriyi Python veri türlerine dönüştürmek için kullanılır. tersi için json.dumps() kullanılır.
        
        exist = Booking.objects.filter(booking_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        
        if exist==False:
            booking = Booking(
                name=data['first_name'],
                booking_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
                no_of_guests = data['guests']
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json') # Django'da HttpResponse kullanırken content_type parametresini belirtmezseniz, varsayılan olarak "text/html" kullanılır. Eğer yanıtınız JSON verisi içeriyorsa, content_type='application/json' olarak belirtmek uygun bir uygulama yöntemidir. Bu, istemci tarafının veriyi JSON olarak algılamasına ve işlemesine yardımcı olur. Örneğin, content_type belirtmeden sadece HttpResponse("{'error':1}") şeklinde kullanırsanız, istemci tarafında JSON içeriği olmasına rağmen veri olarak basit bir metin (string) olarak algılanabilir ve JSON'a ait özel işlemler yapılamayabilir.
    
    date = request.GET.get('date',datetime.today().date()) # gelen istekte "date" bilgisi yoksa bugünün tarihini döner. request.GET.get('param', 'default_value') şeklinde çalışır.  tarih formatı şu şekilde 2023-08-06
    
    bookings = Booking.objects.all().filter(booking_date=date)
    booking_json = serializers.serialize('json', bookings) # queryseti json formatına dönüştürüyorum. xml e de dönüştürmek mümkün.
    
    return HttpResponse(booking_json, content_type='application/json')


class MenuItemView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    ordering_fields = ['price'] # GET istekleri için geçerli sıralama alanlarını belirtir. Kullanıcılar ?ordering=price şeklinde bir sorgu parametresi kullanarak sonuçları fiyata göre sıralayabilirler.
    search_fields = ['title'] # GET istekleri için geçerli arama alanlarını belirtir. Kullanıcılar ?search=title şeklinde bir sorgu parametresi kullanarak menüler arasında başlık (title) alanında arama yapabilirler.
    throttle_classes = [AnonRateThrottle, UserRateThrottle] # Hız sınırlama, belirli bir zaman diliminde API'ye yapılan istek sayısını sınırlamak için kullanılır. AnonRateThrottle, anonim kullanıcıların hızını kontrol ederken, UserRateThrottle, giriş yapmış kullanıcıların hızını kontrol eder.
    
    def get_permissions(self): #Bu, özel izinleri ayarlamak için kullanılan bir fonksiyondur. Bu durumda, GET istekleri için herhangi bir izin gerektirmezken (AllowAny()), POST istekleri için sadece yönetici kullanıcılara izin verir (IsAdminUser()).
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [AllowAny()]


# class MenuViewSet(viewsets.ModelViewSet): # Yukarıdaki kodun ModelViewSet versiyonu. ModelViewSet, tüm CRUD işlemlerini burdan yapılabilmesini imkan verir. fakat generics.ListCreateAPIView sadece get ve post işlemlerinin yapılabilmesine imkan verir. Diğer CRUD işlemleri (güncelleme, silme) için farklı view sınıfları oluşturmanız gerekir.
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
    
#     def get_permissions(self):
#         if self.action == 'create':
#             return [IsAdminUser()]
#         else:
#             return [AllowAny()]
        

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView): #  bu view, yalnızca belirli bir öğenin detaylarını görüntülemek, güncellemek ve silmek için kullanılır. tek bir öğe aldığını url tanımından da teyit edebilirsin.
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            return [IsAdminUser()]
        return [AllowAny()]

      
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action == 'list' or self.action == 'delete':
            if self.request.user.is_authenticated:
                return [IsAuthenticated()]
            else:
                return [IsAdminUser()]
        return [IsAdminUser()]

    # def get_serializer_class(self): # Bu kod bloğu API'de görülebilecek alanları sınırlamak için.
    #     if self.action == 'list':
    #         class ListUserSerializer(BookingSerializer):
    #             class Meta(BookingSerializer.Meta):
    #                 fields = ["no_of_guests", "booking_date"]
    #         return ListUserSerializer
    #     return super().get_serializer_class()


# # djoser kullandığım için user işlemleri için aşağıdaki kod bloğuna gerek kalmadı.
# @api_view(['GET', 'POST']) # bu şekilde aslında APIView'e dönüştürmüş oldum.Ya da aşağıdaki gibi APIView ı kullanarak da yazabilirdim.
# @permission_classes([IsAdminUser]) # permissonlar decorator ile de yapılabilir. Ya da yukarda olduğu gibi get_permission ile özelleştirebilirim.
# def users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)


# class UsersAPIView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# APIView notasyon yapısı:

# class UsersAPIView(APIView):
#     def get(self, request):
#         # GET isteği işleme
#         pass

#     def post(self, request):
#         # POST isteği işleme
#         pass

#     def put(self, request):
#         # PUT isteği işleme
#         pass

#     def delete(self, request):
#         # DELETE isteği işleme
#         pass

from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
#from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer, UserSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html', {})


class MenuItemView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [AllowAny()]


# class MenuViewSet(viewsets.ModelViewSet): # Yukarıdaki kodun ModelViewSet versiyonu
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer
    
#     def get_permissions(self):
#         if self.action == 'create':
#             return [IsAdminUser()]
#         else:
#             return [AllowAny()]
        

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            return [IsAdminUser()]
        return [AllowAny()]

      
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

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
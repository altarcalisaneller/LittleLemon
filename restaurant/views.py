from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

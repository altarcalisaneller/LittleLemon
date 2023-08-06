from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime

from .models import Menu, Booking


class UserSerializer(serializers.ModelSerializer): # User modelini serialize ederken date_joined ekleyerek özelliştirdim. Özelleştirmesydim bu kod bloğuna hiç gerek yoktu. Djoser default bir serialize yapabiliyor zaten.
    Date_Joined = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(write_only=True, default=datetime.now)
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'date_joined', 'Date_Joined']
        
    def get_Date_Joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')

"""
`write_only` özelliği, bir Serializer alanının sadece veri yazmak (göndermek) için kullanılacağını belirtir. Bu özellik, alanın sadece gelen verilerin seri hale getirilmesinde kullanılmasını sağlar, ancak bu alanın dışarı aktarılan (serialize edilen) veriye dahil edilmesini engeller.
Örnekteki `date_joined` alanı `write_only=True` olarak belirtilmiştir. Bu, `date_joined` alanının sadece veri göndermek için kullanıldığını ve dışarı aktarılan (serialize edilen) veriye dahil edilmemesi gerektiğini ifade eder.
Genellikle, `write_only` özelliği, bir Serializer'da gizli veya duyarlı verilerin gönderilmesi için kullanılır. Örneğin, bir kullanıcının şifresini güncellemek için bir API isteği gönderirken, `write_only=True` olarak ayarlanmış bir `password` alanı kullanabilirsiniz. Böylece, şifre verisi API yanıtında görünmez ve sadece veri gönderme amacıyla kullanılır.
Bu özellik, veri güvenliğini sağlamak ve gereksiz bilgilerin dışa aktarılmasını engellemek için kullanışlı olabilir.
"""

"""
SerializerMethodField(), Serializer sınıfında daha sonra tanımlanacak bir yönteme (method) atıfta bulunmak için kullanılır.
Örnekte verilen kod parçasında, Date_Joined adında bir SerializerMethodField() tanımlanmıştır. Bu, Serializer sınıfında get_Date_Joined adında bir yöntem (method) olacağını belirtir.
Bu şekilde, Serializer'da özel hesaplamalar veya veri dönüşümleri yapmak için SerializerMethodField() kullanılabilir. Bu sayede, belirli bir alanın değeri daha karmaşık veya özelleştirilmiş bir şekilde elde edilebilir.
"""
        
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
from rest_framework import serializers
from apps.courses.serializers import PaymentCourseSerializer
from apps.invoices.serializers import InvoiceSerializer

from apps.users.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
class UserExportSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = '__all__'
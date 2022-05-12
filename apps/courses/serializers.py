from rest_framework import serializers

from apps.courses.models import Course

class PaymentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ['id', 'category', 'extra_cost']
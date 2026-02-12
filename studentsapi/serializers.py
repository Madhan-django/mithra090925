from rest_framework import serializers
from admission.models import students

class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = students
        fields = '__all__'

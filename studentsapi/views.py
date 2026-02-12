from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework import status
from global_login_required import login_not_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import studentSerializer
from admission.models import students

# Create your views here.
@login_not_required
@api_view(['GET'])
def studentsapi_home(request):
    try:
        studentdata = students.objects.filter(class_name=2)
        serializer = studentSerializer((studentdata), many=True)
        return Response(serializer.data)
    except Exception as e:
        print("Error :", e)


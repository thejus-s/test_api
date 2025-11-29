from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db import connection
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

BASE_URL = settings.REACT_BASE_URL

@api_view(["POST"])
def signup(request):
    serializer = UserSerilaizer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message":"sigup success",
                "data":serializer.data
            },status=200
        )
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # print(password)
    try:
        userobj = get_object_or_404(User,username=username)
        # print(check_password(userobj.password))
        if check_password(password,userobj.password):
            serializer = UserSerilaizer(userobj)
            refresh = RefreshToken.for_user(userobj)
            return Response(
                {
                    "message": "login success",
                    "status":"success",
                    "data":serializer.data,
                    "userid":userobj.id,
                    "access_token": str(refresh.access_token),
                    "refresh_token" : str(refresh)
                }
            )
        else:
            return Response({
                "error": "invalid password"
            })
    except ObjectDoesNotExist:
        return Response({
                "error": "invalid username"
            })
        
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def addTask(request):
    task = request.data.get('task')
    desc = request.data.get('description')
    try:
            userobj = request.user
            taskobj = Task_List.objects.create(
                user = userobj,
                task = task,
                description = desc
            )
            serializer = TaskSerializer(taskobj)
            return Response({
            "message": "Task added successfully",
            "task": serializer.data,
        },status=200)
    except Exception as e: 
        return Response({
            "error": str(e)
        }, status=500)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def fetchTask(request):
    try:
        userobj = request.user
        tasks = Task_List.objects.filter(user=userobj).order_by("-id")
        serializer = TaskSerializer(tasks, many=True)
        # print(serializer.data)
        return Response(
            {
                "tasks": serializer.data,
            },
            status=200
        )
    except Exception as e:
        return Response({"error": str(e)}, status=500)


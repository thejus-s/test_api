from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","password"]
        extra_kwargs = {
            "password": {"write_only":True},
            "username": {"validators": []}   
        }

    def validate(self,data):
        if  User.objects.filter(username = data["username"]).exists():
             raise serializers.ValidationError({"message":"username already exists"})
        return data
      

    def create(self,validated_data):
       user = User.objects.create_user(
           username=validated_data["username"],
           password=validated_data["password"]
       )
       return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_List
        fields = "__all__"
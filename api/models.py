from django.db import models
from django.contrib.auth.models import User
# class UserData(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)

#     def __str__(self):
#         return self.username

class Task_List(models.Model):
    user = models.ForeignKey(User,related_name='task',on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return (f"{self.user} - {self.task}")
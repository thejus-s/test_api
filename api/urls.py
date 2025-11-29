from django.urls import path,include
from .views import *
urlpatterns = [
    path("signup/",signup,name="signup"),
    path("login/",login,name="login"),
    path("addtask/",addTask,name="addtask"),
    path('fetchtask/',fetchTask,name="fetchtask"),
]

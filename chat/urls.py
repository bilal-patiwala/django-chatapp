from django.urls import path
from . import views
urlpatterns = [
    path('',views.loginUser, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.register, name='register'),
    path('index/', views.index, name='index'),
]
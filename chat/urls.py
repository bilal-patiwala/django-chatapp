from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('searchUser/<str:searchText>',views.searchUser, name='search-user'),
    path('getThread/<str:username>/',views.GetThread.as_view(), name="getThread"),
    path('getMessages/',views.GetMessages.as_view(), name="get_messages"),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.register, name='register'),
    path('index/', views.index, name='index'),
    path("<str:username>/", views.room, name="room"),    
]
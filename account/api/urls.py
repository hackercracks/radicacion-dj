from .views import SignupView
from django.urls import path, include
from .views import CustomAuthToken, UserListView, UserDetail

urlpatterns = [
    path('rest-auth/registration/', SignupView.as_view()),
    path('rest-auth/login/', CustomAuthToken.as_view(), name ='auth-token'),
    path('rest-auth/', include('rest_auth.urls')),
    path('userlist/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]


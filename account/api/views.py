from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import UserSerializer, SignupSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from account.models import User, FailedLogin

# from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

@receiver(user_logged_in)
def user_logged_recv(sender, request, user, **kwargs):
    FailedLogin.objects.filter(user=user).delete()

@receiver(user_login_failed)
def user_login_failed_recv(sender, credentials, request, **kwargs):
    # User = get_user_model()
    try:
        u = User.objects.get(username = credentials.get('username'))
        # there is a user with the given username
        FailedLogin.objects.create(user=u)
        if FailedLogin.objects.filter(user=u).count() >= 3:
            # three tries or more, disactivate the user
            u.is_active = False
            u.save()
    except User.DoesNotExist:
        # user not found, we can not do anything
        pass



class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token": Token.objects.get(user=user).key,
            "message": "account create successfully"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token":token.key,
            "user_id": user.pk,
            "is_organisor": user.is_organisor,
            "is_agent": user.is_agent,
            "is_support": user.is_support,
            "username": user.username,
            "email": user.email,
        })


class UserListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
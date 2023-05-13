from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import AgentSignUpSerializer
from account.models import User, UserProfile
from filed.models import Agent

from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from agents.tokens import account_activation_token
from rest_framework.views import APIView


class CreateAgentView(generics.GenericAPIView):
    serializer_class = AgentSignUpSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.is_support == True:
            UserProfile.objects.create(user=user)
        if user.is_agent == True:
            Agent.objects.create(
            user=user,
            organisation= self.request.user.userprofile
        )

        # ====== send email notification ===== #
        email = user.email
        subject= 'Activate Your SLDC Account'
        from_email= settings.EMAIL_HOST_USER
        html_template = 'account/account_activation_email.html'

        html_message = render_to_string(html_template, {
                'user': user,
                'domain': '127.0.0.1:3000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

        message = EmailMessage(subject, html_message, from_email, [email])
        message.content_subtype = 'html' # this is required because there is no plain text email version
        message.send()

        return Response({
            "user": AgentSignUpSerializer(user, context=self.get_serializer_context()).data,
            # "token": Token.objects.get(user=user).key,
            "message": "account create successfully"
        })


class ActivateView(APIView):
    def post(self, request, uidb64, token):

        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            
# <<<<<<< HEAD
            return Response({
                "message": "Your account has been activated successfully"
                })
# =======
            return Response("Your account has been activated now")
# >>>>>>> 41d075ff9767a8928ee7b24f76954159388e6cc1
        else:
            return Response("Oops! something is wrong")

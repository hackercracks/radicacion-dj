from rest_framework import serializers
from account.models import User, UserProfile

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class AgentSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password', 'is_agent', 'is_support']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']

        user.set_password(password)
        user.is_agent= self.validated_data['is_agent']
        user.is_support= self.validated_data['is_support']
        user.is_organisor = False
        user.is_active = False

        value = user.email

        try:
            validate_email(value)
        except ValidationError as e:
            print("bad email, details:", e)
        else:
            print("good email")

        user.save()
        return user


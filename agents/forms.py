from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )
        widgets = {
            'email' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'username' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'first_name' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name' : forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

class RemoveUser(forms.Form):
    username = forms.CharField()
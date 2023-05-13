import random

from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, render, redirect
from filed.models import Agent
from .forms import AgentModelForm, RemoveUser
from account.models import UserProfile
from django.conf import settings

from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from django.contrib.auth import login, authenticate
# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token


from django.contrib.auth import get_user_model
User = get_user_model()


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_agent = True
        user.is_organisor = False
        # pasw = random.randint(0, 1000000)
        # user.set_password(f"{pasw}")
        user.set_password(f"test12345")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )

        messages.success(self.request, "Agent created successfully")

        # ====== send email notification ===== #
        email = user.email
        subject= 'Activate Your SLDC Account'
        # message= f"password:- test12345 You were added as an agent on SLCD_CRM. Please come login to start working. "
        # message = render_to_string('account/account_activation_email.html', {
        #         'user': user,
        #         'domain': '127.0.0.1:8000',
        #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #         'token': account_activation_token.make_token(user),
        #     })
        from_email= settings.EMAIL_HOST_USER
        recipient_list=[email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)


        html_version = 'account/account_activation_email.html'

        html_message = render_to_string(html_version, {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

        message = EmailMessage(subject, html_message, from_email, [email])
        message.content_subtype = 'html' # this is required because there is no plain text email version
        message.send()

        return super(AgentCreateView, self).form_valid(form)


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):

    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    #user = User.objects.get(pk=uid)
    try:

        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return render(request, 'account/homeacttive.html',{'subject': user})
    else:
        return render(request, 'account/register.html')

class SupportCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/support_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_support = True
        user.is_organisor = False
        # pasw = random.randint(0, 1000000)
        # user.set_password(f"{pasw}")
        user.set_password(f"test12345")
        # user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        # Agent.objects.create(
        #     user=user,
        #     organisation=self.request.user.userprofile
        # )
        # Create the user profile
        UserProfile.objects.create(user=user)

        messages.success(self.request, "Support created successfully")


        # ====== send email notification ===== #
        email = user.email
        subject= 'You are invited to be an support'
        # message= f"password:- test12345 You were added as an support on SLCD_CRM. Please come login to start working. "
        message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        from_email= settings.EMAIL_HOST_USER
        recipient_list=[email]

        html_version = 'account/account_activation_email.html'

        html_message = render_to_string(html_version, {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

        message = EmailMessage(subject, html_message, from_email, [email])
        message.content_subtype = 'html' # this is required because there is no plain text email version
        message.send()
        return super(SupportCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


def Agent_Delete(request, pk):  
    print(pk)
    try:
        u = User.objects.get(id = pk)
        u.delete()
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "Agent User doesnot exist")    
        return render(request, 'agents/agent_list.htmll')

    except Exception as e: 
        return render(request, 'agents/agent_list.html',{'err':e.message})

    return redirect('agents:agent-list')

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import UserProfile
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

import random



def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/files')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username=cd['username'],
            password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # return HttpResponse('Authenticated successfully')
                messages.success(request, "Logged in successfully")
                return redirect("/files")
            else:
                # return HttpResponse('Disabled account')
                messages.error(request, "Disabled account")
                return redirect("/login")

        else:
            messages.error(request, "Invalid login details or Your account has not been activated")
            return redirect("/login")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def landingPage(request):
    return render(request, "landingPage.html")

@login_required
def dashboard(request):
    return render(request,
    'account/dashboard.html',
    {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save() 
            # Create the user profile
            UserProfile.objects.create(user=new_user)
            # return render(request, 'account/register_done.html', {'new_user': new_user})

            messages.success(request, "Account created successfully")


            # ====== send email notification ===== #
            username = request.POST['username']
            email = request.POST['email']
            subject = 'Successfully created an account'
            message = f'Hi {username} welcome to SLCD enjoy the experince on the site'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)


            # message.success(request, "Account created successfully")
            return redirect("/login")
        else:
            messages.error(request, "details already in used")
            return redirect("register")
            # return HttpResponse('username already in use')
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
        data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{'user_form': user_form, 
                    'profile_form': profile_form})        
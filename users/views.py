"""Django Views for Users."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.core.files.storage import FileSystemStorage
from .forms import UserRegisterForm, UserCreateMeetForm

from .forms import UserRegisterForm, UserCreateMeetForm, UserUpdateDetailForm, ProfileUpdateForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from appointment.models import UserMeeting


def register(request):
    """Render to register page if user is already logged in, redirect to home page."""
    if request.user.is_authenticated:
        messages.info(request, 'You have to logout before make a new register')
        return redirect('appointment:home_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} has been created!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class LoginFormView(SuccessMessageMixin, LoginView):
    """User login page."""

    template_name = 'users/login.html'
    success_url = 'appointment:home_page'
    success_message = "You were successfully logged in."


@login_required
def edit_profile(request):
    """Render to profile.html."""
    if request.method == 'POST':
        user_update_form = UserUpdateDetailForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your profile has been update!!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateDetailForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_update_form': user_update_form, 'profile_update_form': profile_update_form}
    return render(request, 'users/edit_profile.html', context)


def other_profiles(request, user_id):
    """View the other profiles."""
    specific_user = get_object_or_404(User, pk=user_id)
    joining_meet = UserMeeting.objects.filter(user=specific_user, is_join=True)
    return render(request, 'users/other_profiles.html', {'specific_user': specific_user, 'joining_meet': joining_meet})


@login_required
def profile(request):
    """Edit your profiles."""
    profile_info = ["Username", "Email", "University", "Address"]
    user_profile = [request.user.username, request.user.email,
                    request.user.profile.university, request.user.profile.address]
    context = {"user_profile": user_profile, "profile_info": profile_info}

    return render(request, 'users/profile.html', context)

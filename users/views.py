from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView

def register(request):
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
    return render(request, 'users/register.html', {'form' : form})

class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_url = 'appointment:home_page'
    success_message = "You were successfully logged in."

@login_required
def profile(request):
    return render(request, 'users/profile.html')
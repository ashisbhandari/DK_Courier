from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.hashers import check_password
from .forms import SignupForm
from .models import Signup
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

from django.contrib.auth.hashers import check_password


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Update with your actual login route name
    else:
        form = SignupForm()
    return render(request, 'courier/signup.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Signup

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    login(request, user)  # sets session
                    return redirect('/Admin/')  # or reverse('dashboard')
                else:
                    messages.error(request, "Account is inactive.")
            else:
                messages.error(request, "Incorrect password.")
        except Signup.DoesNotExist:
            messages.error(request, "No user found with this email.")

    return render(request, 'courier/login.html')

# logout also kills session
def user_logout(request):
    logout(request)
    return redirect('/')
def home(request):
    return render(request,'courier/home.html')
def navbar(request):
    return render(request,'courier/dash-nav.html')
# @login_required(login_url='/Login/')
def dashboard(request):
    return render(request, 'courier/dashboard.html')
def check(request):
    return render(request,'courier/check.html')
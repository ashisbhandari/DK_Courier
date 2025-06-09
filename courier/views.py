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
from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request,'courier/index.html')
def navbar(request):
    return render(request,'courier/dash-nav.html')
# @login_required(login_url='/Login/')
def dashboard(request):
    return render(request, 'courier/dashboard.html')

from .models import BookingList
def check(request):
    bookings = BookingList.objects.all()  # fetch all rows
    context = {
        'bookings': bookings
    }
    return render(request, 'courier/check.html', context)

from .forms import BookingForm

def bookdoc(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Access data with form.cleaned_data
            # Save or process booking
            messages.success(request, "Booking successfully submitted!")
            return redirect('some-view-name')
        else:
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()

    return render(request, 'courier/bookdoc.html', {'form': form})


from .models import BookingForm
from .forms import BookingFormForm
def book_edit(request, pk):
    booking = get_object_or_404(booking, pk=pk)
    context = {'booking': booking}
    return render(request, 'courier/edit_booking.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
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

# def check(request):
#     bookings = BookingList.objects.all().order_by('-date')  # You can filter/search here later
#     return render(request, 'courier/check.html',{
#         'bookings': bookings,
#     })

from django.shortcuts import render
from .models import BookingList

def check(request):
    bookings = BookingList.objects.all()

    total_shipments = bookings.count()
    total_cash = bookings.filter(payments='Cash').count()
    total_cod = bookings.filter(payments='COD').count()
    total_credit = bookings.filter(payments='Credit').count()

    context = {
        'bookings': bookings,
        'total_shipments': total_shipments,
        'total_cash': total_cash,
        'total_cod': total_cod,
        'total_credit': total_credit,
    }
    return render(request, 'courier/check.html', context)


from .forms import BookingForm 
def bookdoc(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        form = BookingForm() 
    return render(request, 'courier/bookdoc.html', {'form': form})

def book_edit(request):  
    return render(request, 'courier/edit_booking.html')
from django.shortcuts import render, get_object_or_404
from .models import PdfParcel

def pkt_pdf(request, cn_no):  # Get cn_no from URL param
    parcel = get_object_or_404(PdfParcel, CN_No=cn_no)
    return render(request, 'courier/pdf.html', {'row': parcel})

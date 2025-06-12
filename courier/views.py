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
def dashboard1(request):
    bookings = BookingList.objects.order_by('-id')

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
    return render(request, 'courier/check.html',context)


from .models import BookingList
from django.shortcuts import render


# def dashboard(request):
#     bookings = BookingList.objects.order_by('-id')

#     total_shipments = bookings.count()
#     total_cash = bookings.filter(payments='Cash').count()
#     total_cod = bookings.filter(payments='COD').count()
#     total_credit = bookings.filter(payments='Credit').count()

#     context = {
#         'bookings': bookings,
#         'total_shipments': total_shipments,
#         'total_cash': total_cash,
#         'total_cod': total_cod,
#         'total_credit': total_credit,
#     }
#     return render(request, 'courier/dashboard.html', context)

from django.shortcuts import render
def dashboard(request):
    sender_name = request.GET.get('sender_name', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    # Base queryset - all bookings
    bookings = BookingList.objects.order_by('-id')

    # Filter by sender_name if provided
    if sender_name:
        bookings = bookings.filter(sname__icontains=sender_name)

    # Filter by start_date if provided
    if start_date:
        bookings = bookings.filter(date__gte=start_date)

    # Filter by end_date if provided
    if end_date:
        bookings = bookings.filter(date__lte=end_date)

    # Calculate totals for dashboard cards based on filtered queryset or overall
    total_shipments = bookings.count()
    total_cash = bookings.filter(payments='Cash').count()
    total_cod = bookings.filter(payments='COD').count()
    total_credit = bookings.filter(payments='Credit').count()

    context = {
        'bookings': bookings.order_by('-date'),  # Show latest first
        'total_shipments': total_shipments,
        'total_cash': total_cash,
        'total_cod': total_cod,
        'total_credit': total_credit,
        'request': request,  # pass request for form values in template
    }
    return render(request, 'courier/dashboard.html', context)


from django.shortcuts import render, get_object_or_404
from .models import PdfParcel
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

def book_edit(request, cn_no):
    parcel = get_object_or_404(PdfParcel, CN_No=cn_no)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=parcel)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        form = BookingForm(instance=parcel)
    return render(request, 'courier/edit.html', {'row': parcel, 'form': form})


# customer bills pdf
def pkt_pdf(request, cn_no):  # Get cn_no from URL param
    parcel = get_object_or_404(PdfParcel, CN_No=cn_no)
    return render(request, 'courier/pdf.html', {'row': parcel})
# bank bills pdf without cash and weight
def pkt_pdf1(request, cn_no):  # Get cn_no from URL param
    parcel = get_object_or_404(PdfParcel, CN_No=cn_no)
    return render(request, 'courier/pdf1.html', {'row': parcel})

# invoice pdf
# from django.http import HttpResponse

# def invoice(request):
#     return render(request,"courier/invoice.html")


from .models import PdfParcel  # replace with your actual model name

from django.shortcuts import render, get_list_or_404
def invoice(request):
    cn_nos = request.GET.get('cn_no')
    if not cn_nos:
        return render(request, 'courier/invoice.html', {
            'error': 'No CN numbers provided.'
        })

    cn_list = cn_nos.split(',')
    # Fetch bookings with given CN numbers, or return 404 if any missing
    bookings = get_list_or_404(BookingList, cn_no__in=cn_list)

    # You can customize the invoice data here as needed
    context = {
        'bookings': bookings,
        'cn_nos': cn_list,
    }
    return render(request, 'courier/invoice.html', context)


def courier_bill(request):
    cn_nos = request.GET.get('cn_no')
    if not cn_nos:
        return render(request, 'courier/invoice.html', {
            'error': 'No CN numbers provided.'
        })

    cn_list = cn_nos.split(',')
    bookings = get_list_or_404(BookingList, cn_no__in=cn_list)
    context = {
        'bookings': bookings,
        'cn_nos': cn_list,
    }
    return render(request, 'courier/bills.html', context)
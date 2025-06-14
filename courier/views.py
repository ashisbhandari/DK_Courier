from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignupForm
from django.contrib.auth import logout
from .models import Signup
from django.contrib import messages
from .forms import ComplaintForm
from django.contrib.auth import login as auth_login  # alias to avoid confusion
from django.views.decorators.cache import never_cache



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Update with your actual login route name
    else:
        form = SignupForm()
    return render(request, 'courier/signup.html', {'form': form})



@never_cache
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    auth_login(request, user)  # now calls Django's login correctly
                    messages.success(request, "Login successful!")
                    return redirect('/dashboard')
                else:
                    messages.error(request, "Account is inactive.")
            else:
                messages.error(request, "Incorrect password.")
        except Signup.DoesNotExist:
            messages.error(request, "User does not exist.")
    return render(request, 'courier/login.html')


# logout also kills session
def user_logout(request):
    logout(request)
    return redirect('/')
def home(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your complaint has been submitted successfully!")
            return redirect('/')  # You can change this to a thank-you page if you want
    else:
        form = ComplaintForm()
    return render(request,'courier/index.html')
def navbar(request):
    return render(request,'courier/dash-nav.html')
# @login_required(login_url='/Login/')
# def dashboard1(request):
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
#     return render(request, 'courier/check.html',context)


from .models import BookingList

from django.contrib.auth.decorators import login_required

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
@login_required(login_url='/Login/') 
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

@login_required(login_url='/Login/') 
def bookdoc(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        form = BookingForm() 
    return render(request, 'courier/bookdoc.html', {'form': form})


@login_required(login_url='/Login/') 
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

@login_required(login_url='/Login/') 
def pkt_pdf(request, cn_no):  # Get cn_no from URL param
    parcel = get_object_or_404(PdfParcel, CN_No=cn_no)
    return render(request, 'courier/pdf.html', {'row': parcel})
# bank bills pdf without cash and weight

@login_required(login_url='/Login/') 
def pkt_pdf1(request, cn_no):  # Get cn_no from URL param
    parcel = get_object_or_404(PdfParcel, CN_No=cn_no)
    return render(request, 'courier/pdf1.html', {'row': parcel})

# invoice pdf
# from django.http import HttpResponse

# def invoice(request):
#     return render(request,"courier/invoice.html")


from .models import PdfParcel  # replace with your actual model name

from django.shortcuts import render, get_list_or_404

@login_required(login_url='/Login/') 
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


@login_required(login_url='/Login/') 
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

# def complain(request):
#     return render(request, 'courier/complain_box.html')
from django.shortcuts import render
from .models import Complaint

# def complain(request):
#     complains = Complaint.objects.all().order_by('-id')
#     return render(request, 'courier/complain_box.html', {'complains': complains})
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Complaint

def complain(request):
    complains = Complaint.objects.all().order_by('-id')
    return render(request, 'courier/complain_box.html', {'complains': complains})

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        message = data.get('message')

        # Fetch complaint
        complaint = Complaint.objects.filter(email=email).order_by('-date_submitted').first()
        if not complaint:
            return JsonResponse({'error': 'Complaint not found'}, status=404)

        # Email sending
        subject = "Thank you for your feedback - DK Courier"
        html_content = f"""
        <html>
        <body style="font-family: Arial; padding: 10px;">
            <h3 style="color: orange;">DK Courier</h3>
            <p>{message}</p>
            <hr>
            <small>This is an automated reply from DK Courier.</small>
        </body>
        </html>
        """
        email_obj = EmailMessage(subject, html_content, "your_email@example.com", [email])
        email_obj.content_subtype = "html"
        email_obj.send()

        # Mark complaint as replied
        complaint.replied = True
        complaint.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

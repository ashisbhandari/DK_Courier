from django import forms
from django.core.exceptions import ValidationError
from .models import Signup

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}), label="Confirm Password")

    class Meta:
        model = Signup
        fields = ['company_name', 'address', 'ownername', 'email', 'contact', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Signup.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Enter password'}))
    
    
    
from .models import Booking_list

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking_list
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'country': forms.Select(choices=[(c, c) for c in "Nepal India UAE Australia Canada Qatar Saudi Arebia USA".split()]),
            'district': forms.Select(choices=[(d, d) for d in "acham arghakhanchi baglung bajhang bajura baitadi banke bardiya bara Bhaktapur bhojpur chitwan dadeldhura Dang dailekh darchula dhading dhankuta dhanusha dolakha dolpa doti eastern_rukum gulmi gorkha humla ilam jhapa jajarkot jumla Kathmandu kanchanpur kailali kalikot kapilvastu kaski khotang kavrepalanchok lalitpur lamjung mahendranagar mahottari makwanpur manang morang mugu myagdi mustang nawalpur east-nawalparasi west-nawalparasi nuwakot okhaldhunga parbat parsa pachthar palpa pyuthan rajbiraj rautahat ramechap rasuwa Rupandehi Rolpa salyan sankhuwasabha saptari sarlahi sindhuli sindhupalchok siraha solukhumbu sunsari Surkhet Syangja tanahun taplejung terhathum udayapur western_rukum".split()]),
            'pactype': forms.Select(choices=[('', '--None--'), ('Document', 'Document'), ('Parcel', 'Parcel')]),
            'payments': forms.Select(choices=[('Cash', 'Cash'), ('Credit', 'Credit'), ('COD', 'COD')]),
            'service': forms.Select(choices=[('Door to Door', 'Door to Door'), ('Office Collect', 'Office Collect')]),
        }
        
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'contact', 'email', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name here...'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9812345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'DKCourier@gmail.com'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comments here...'}),
        }
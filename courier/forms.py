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
from django import forms

class BookingForm(forms.Form):
    country = forms.ChoiceField(
        choices=[
            ('', 'Select Country'),
            ('Nepal', 'Nepal'),
            ('India', 'India'),
            ('UAE', 'UAE'),
            ('Australia', 'Australia'),
            ('Canada', 'Canada'),
            ('Qatar', 'Qatar'),
            ('Saudi Arebia', 'Saudi Arebia'),
            ('USA', 'USA'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'countrySelect'})
    )

    district = forms.ChoiceField(
        choices=[
            ('', 'Select District'),
            ('acham', 'Acham'),
            ('arghakhanchi', 'Arghakhanchi'),
            ('baglung', 'Baglung'),
            ('bajhang', 'Bajhang'),
            ('bajura', 'Bajura'),
            ('baitadi', 'Baitadi'),
            ('banke', 'Banke'),
            ('bardiya', 'Bardiya'),
            ('bara', 'Bara'),
            ('Bhaktapur', 'Bhaktapur'),
            ('bhojpur', 'Bhojpur'),
            ('chitwan', 'Chitwan'),
            ('dadeldhura', 'Dadeldhura'),
            ('Dang', 'Dang'),
            ('dailekh', 'Dailekh'),
            ('darchula', 'Darchula'),
            ('dhading', 'Dhading'),
            ('dhankuta', 'Dhankuta'),
            ('dhanusha', 'Dhanusha'),
            ('dolakha', 'Dolakha'),
            ('dolpa', 'Dolpa'),
            ('doti', 'Doti'),
            ('eastern_rukum', 'Eastern Rukum'),
            ('gulmi', 'Gulmi'),
            ('gorkha', 'Gorkha'),
            ('humla', 'Humla'),
            ('ilam', 'Ilam'),
            ('jhapa', 'Jhapa'),
            ('jajarkot', 'Jajarkot'),
            ('jumla', 'Jumla'),
            ('Kathmandu', 'Kathmandu'),
            ('kanchanpur', 'Kanchanpur'),
            ('kailali', 'Kailali'),
            ('kalikot', 'Kalikot'),
            ('kapilvastu', 'Kapilvastu'),
            ('kaski', 'Kaski'),
            ('khotang', 'Khotang'),
            ('kavrepalanchok', 'Kavrepalanchok'),
            ('lalitpur', 'Lalitpur'),
            ('lamjung', 'Lamjung'),
            ('mahendranagar', 'Mahendranagar'),
            ('mahottari', 'Mahottari'),
            ('makwanpur', 'Makwanpur'),
            ('manang', 'Manang'),
            ('morang', 'Morang'),
            ('mugu', 'Mugu'),
            ('myagdi', 'Myagdi'),
            ('mustang', 'Mustang'),
            ('nawalpur', 'Nawalpur'),
            ('east-nawalparasi', 'East-Nawalparasi'),
            ('west-nawalparasi', 'West-Nawalparasi'),
            ('nuwakot', 'Nuwakot'),
            ('okhaldhunga', 'Okhaldhunga'),
            ('parbat', 'Parbat'),
            ('parsa', 'Parsa'),
            ('pachthar', 'Pachthar'),
            ('palpa', 'Palpa'),
            ('pyuthan', 'Pyuthan'),
            ('rajbiraj', 'Rajbiraj'),
            ('rautahat', 'Rautahat'),
            ('ramechap', 'Ramechap'),
            ('rasuwa', 'Rasuwa'),
            ('Rupandehi', 'Rupandehi'),
            ('Rolpa', 'Rolpa'),
            ('salyan', 'Salyan'),
            ('sankhuwasabha', 'Sankhuwasabha'),
            ('saptari', 'Saptari'),
            ('sarlahi', 'Sarlahi'),
            ('sindhuli', 'Sindhuli'),
            ('sindhupalchok', 'Sindhupalchok'),
            ('siraha', 'Siraha'),
            ('solukhumbu', 'Solukhumbu'),
            ('sunsari', 'Sunsari'),
            ('Surkhet', 'Surkhet'),
            ('Syangja', 'Syangja'),
            ('tanahun', 'Tanahun'),
            ('taplejung', 'Taplejung'),
            ('terhathum', 'Terhathum'),
            ('udayapur', 'Udayapur'),
            ('western_rukum', 'Western Rukum'),
        ],
        required=False,  # Will be required only if country == Nepal, handle in form clean()
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'districtSelect'})
    )

    pactype = forms.ChoiceField(
        choices=[
            ('', '--None--'),
            ('Document', 'Document'),
            ('Parcel', 'Parcel'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'id': 'realDateTextBox'})
    )

    # Sender details
    Sname = forms.CharField(max_length=100, required=True)
    Snumber = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[0-9]{10}'})
    )
    Saddress = forms.CharField(max_length=255, required=True)
    Saddress1 = forms.CharField(max_length=255, required=False)

    # Receiver details
    Rname = forms.CharField(max_length=100, required=True)
    Rnumber = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'pattern': '[0-9]{10}'})
    )
    Raddress = forms.CharField(max_length=255, required=True)
    Raddress1 = forms.CharField(max_length=255, required=False)

    # Package & Payment info
    payments = forms.ChoiceField(
        choices=[('Cash', 'Cash'), ('Credit', 'Credit'), ('COD', 'COD')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    service = forms.ChoiceField(
        choices=[('Door to Door', 'Door to Door'), ('Office Collect', 'Office Collect')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    price = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True, initial=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    weight = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    pieces = forms.IntegerField(required=True, initial=1)
    Bookby = forms.CharField(max_length=100, required=False, initial='ko hola')

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        district = cleaned_data.get('district')

        if country == 'Nepal' and not district:
            self.add_error('district', 'District is required when country is Nepal.')

        return cleaned_data

        
from .models import BookingForm

class BookingFormForm(forms.ModelForm):
    class Meta:
        model = BookingForm
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'country': forms.Select(choices=[(c, c) for c in "Nepal India UAE Australia Canada Qatar Saudi Arebia USA".split()]),
            'district': forms.Select(choices=[(d, d) for d in "acham arghakhanchi baglung bajhang bajura baitadi banke bardiya bara Bhaktapur bhojpur chitwan dadeldhura Dang dailekh darchula dhading dhankuta dhanusha dolakha dolpa doti eastern_rukum gulmi gorkha humla ilam jhapa jajarkot jumla Kathmandu kanchanpur kailali kalikot kapilvastu kaski khotang kavrepalanchok lalitpur lamjung mahendranagar mahottari makwanpur manang morang mugu myagdi mustang nawalpur east-nawalparasi west-nawalparasi nuwakot okhaldhunga parbat parsa pachthar palpa pyuthan rajbiraj rautahat ramechap rasuwa Rupandehi Rolpa salyan sankhuwasabha saptari sarlahi sindhuli sindhupalchok siraha solukhumbu sunsari Surkhet Syangja tanahun taplejung terhathum udayapur western_rukum".split()]),
            'pactype': forms.Select(choices=[('', '--None--'), ('Document', 'Document'), ('Parcel', 'Parcel')]),
            'payments': forms.Select(choices=[('Cash', 'Cash'), ('Credit', 'Credit'), ('COD', 'COD')]),
            'service': forms.Select(choices=[('Door to Door', 'Door to Door'), ('Office Collect', 'Office Collect')]),
        }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import finger_image,face_image,qr_image,Rating
from .models import Profile

from django.db import models
class RegisterForm(UserCreationForm):
    
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Tên đăng nhập',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Nhập lại mật khẩu',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class FingerImageForm(forms.ModelForm):  

    class Meta:  
        model = finger_image
        fields = [ 'image']


class FaceImageForm(forms.ModelForm):  

    class Meta:  
        model = face_image
        fields = ['image']

class QRForm(forms.ModelForm):  

    class Meta:  
        model = qr_image
        fields = ['image','bill']


thansohoc_CHOICES = [
    ('0', '0 VNĐ'),
    ('1', '50.000 VNĐ'),
    ('5', '225.000 VNĐ'),
    ('10', '400.000 VNĐ'),
]
nhantuonghoc_CHOICES = [
    ('0', '0 VNĐ'),
    ('1', '80.000 VNĐ'),
    ('5', '360.000 VNĐ'),
    ('10', '640.000 VNĐ'),
]

sinhtrachoc_CHOICES = [
    ('0', '0 VNĐ'),
    ('1', '100.000 VNĐ'),
    ('5', '450.000 VNĐ'),
    ('10', '800.000 VNĐ'),
]

SERVICE_CHOICES = [
    ('0', ''),
    ('1', ''),
    ('5', ''),
    ('10', ''),
]
class UpgradeForm(forms.Form):
    thansohoc = forms.ChoiceField(choices=thansohoc_CHOICES, widget=forms.RadioSelect, label='Thần số học')
    
    
    nhantuonghoc = forms.ChoiceField(choices=nhantuonghoc_CHOICES, widget=forms.RadioSelect, label='Nhân tướng học')
    sinhtrachoc = forms.ChoiceField(choices=sinhtrachoc_CHOICES, widget=forms.RadioSelect, label='Sinh trắc học')
    tuvan = forms.ChoiceField(choices=SERVICE_CHOICES, widget=forms.RadioSelect, label='Dịch vụ tư vấn 1:1')


class BankDetailsForm(forms.Form):
    bank = forms.ChoiceField(choices=[], required=False, label="Bank")
    account_number = forms.CharField(max_length=20, required=False, label="Account Number")

    def __init__(self, *args, **kwargs):
        bank_choices = kwargs.pop('bank_choices', [])

        super(BankDetailsForm, self).__init__(*args, **kwargs)
        self.fields['bank'].choices = bank_choices


class StarRadioSelect(forms.RadioSelect):
    template_name = 'widgets/radio.html'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
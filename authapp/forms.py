from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from authapp.models import UserUsername, UserPrimaryEmail

from PIL import Image
from django.core.files import File
from .models import UserPhoto, STATUS_CHOICES


class UserCreateForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username(id)'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'password_confirm'}))

    year = forms.IntegerField(initial='', widget=forms.Select(attrs={'class': 'form-control', 'id': 'years', 'placeholder': 'Year'}), required=True)
    month = forms.IntegerField(initial='', widget=forms.Select(attrs={'class': 'form-control', 'id': 'months', 'placeholder': 'Month'}), required=True)
    day = forms.IntegerField(initial='', widget=forms.Select(attrs={'class': 'form-control', 'id': 'days', 'placeholder': 'Day'}), required=True)
    gender = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect(), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'year', 'month', 'day', 'gender']


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control login-form',
                                                             'placeholder': 'username(id) or email',
                                                             'id': 'id_username_login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control login-form',
                                                                 'placeholder': 'password',
                                                                 'id': 'id_password_login'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class EmailAddForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'enter email to add'}))

    class Meta:
        model = User
        fields = ['email']


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'new Password'}))
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'new Password confirm'}))

    class Meta:
        model = User
        fields = ['password']


class PasswordResetForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username(ID) or Email'}))

    class Meta:
        model = User
        fields = ['username']


class PasswordResetConfirmForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'new Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'new Password confirm'}))

    class Meta:
        model = User
        fields = ['password']


class PasswordCheckBeforeDeactivationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['password']


class PasswordCheckBeforeDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['password']

class PasswordChangeWithUserPKForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput(
        attrs={'class': 'form-control', 'placeholder': 'username(id)'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'new Password'}))
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'new Password confirm'}))

    class Meta:
        model = User
        fields = ['pk', 'password']


class UserPhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    rotate = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserPhoto
        fields = ('file_300', 'file_50', 'x', 'y', 'width', 'height', 'rotate',)

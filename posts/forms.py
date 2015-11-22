
# -*- coding: utf-8 -*-
from django import forms
from posts.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label = "Senha antiga", widget=forms.PasswordInput())

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u"Digite corretamente a senha")
        return old_password

class SetNewPasswordForm(ChangePasswordForm):
    password = forms.CharField(label = 'Nova senha', widget = forms.PasswordInput())
    confirm_password = forms.CharField(label = 'Confirme nova senha', widget = forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(u"Digite senhas iguais")
        return confirm_password
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password"])
        if commit:
            self.user.save()
        return self.user

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())

class UserForm(forms.ModelForm):

    username = forms.RegexField(max_length = 30, regex=r'^[\w.@+-]+$')
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
        'email', 'username',
        'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Senha'
        self.fields['confirm_password'].label = 'Confirme sua senha'
        self.fields['first_name'].label = 'Nome'
        self.fields['last_name'].label = 'Sobrenome'
        self.fields['email'].label = 'E-mail'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact = username).exists():
            raise forms.ValidationError(u'Username já cadastrado!')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(u'As senhas não batem!')
        return confirm_password

    def save(self, commit = True):
        user = super(UserForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['photo'].label = 'Escolha uma foto'
        self.fields['description'].label = 'Descrição'
        self.fields['cover_photo'].label = 'Foto de Capa'

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ReaderForm, self).__init__(*args, **kwargs)
        self.fields['photo'].label = 'Escolha uma foto'

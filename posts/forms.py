
# -*- coding: utf-8 -*-
from django import forms
from posts.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages

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

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['author', 'date_time']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = u'Título'
        self.fields['content'].label = 'Escreva seu texto aqui'

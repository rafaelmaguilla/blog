# Create your views here.
# -*- coding: utf-8 -*-
import mimetypes, os
from datetime import *
from os import path
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from forms import *
from django.template import RequestContext, loader, Context
from posts.forms import *
from posts.models import *
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
from django.views.generic import View, TemplateView
#from django.core.mail import *
from django.db.models import Q, F
from django.http import HttpResponseRedirect as redirect
from django.contrib.auth.decorators import *
from posts.forms import *

# Create your views here.

def highlight_errors(request, form_list):
	for form in form_list:
		for field in form:
			if field.errors:
				print(str(field.errors))

class Login(View):
	post = False
	def get(self, request):
		if not self.post:
			login_form = self.login_form()
			if request.user.is_authenticated():
				return redirect(self.redirect_to)
		else:
			login_form = self.login_form(request.POST)
		return render(request, self.template, locals())

	def post(self, request):
		login_form = self.login_form(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(self.redirect_to)
			else:
				print('Sua conta foi desativada!')
		else:
			print('Username e/ou senha incorreto(s)')
		return render(request, self.template, locals())

class Logout(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return redirect(self.redirect_to)

    def post (self, request):
        if request.user.is_authenticated():
            logout(request)
        return redirect(self.redirect_to)

class LoginAuthor(Login):
	login_form = LoginForm
	template = 'login_author.html'
	redirect_to = '/list_authors'

class LogoutAuthor(Logout):
	redirect_to = '/login_author'

class CreateUser(View):
	post = False
	user_form = UserForm

	def get(self, request):
		if not self.post:
			object_form = self.object_form()
			user_form = self.user_form()
		else:
			object_form = self.object_form(request.POST)
			user_form = self.user_form(request.POST)
		return render(request, self.template, locals())

	def post(self, request):
		self.post = True
		object_form = self.object_form(request.POST)
		user_form = self.user_form(request.POST)
		if user_form.is_valid() and object_form.is_valid():
			new_object = object_form.save(commit = False)
			new_user = user_form.save()
			new_object.user = new_user
			new_object.save()
			return redirect(self.redirect_to)
		else:
			return self.get(request)

class CreateAuthor(CreateUser):
	object_form = AuthorForm
	template = 'new_author.html'
	redirect_to = '/list_authors'

class ListAuthors(View):
	def get(self, request):
		qs_authors = Author.objects.all().order_by('user__first_name')
		return render(request, 'list_authors.html', locals())

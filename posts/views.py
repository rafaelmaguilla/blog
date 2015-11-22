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
from django.core.validators import validate_email
# Create your views here.

def highlight_errors(request, form_list):
	for form in form_list:
		for field in form:
			if field.errors:
				print(str(field.errors))

######## CLASSES ABSTRATAS
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
				messages.error(request, u'Sua conta foi está desativada!')
		else:
			messages.error(request, 'Username e/ou senha incorreto(s)')
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

class CreateUser(View):
	post = False
	user_form = UserForm

	def get(self, request):
		if not self.post:
			object_form = self.object_form()
			user_form = self.user_form()
		else:
			object_form = self.object_form(request.POST, request.FILES)
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
			messages.success(request, self.success_message)
			return redirect(self.redirect_to)
		else:
			return self.get(request)

class ChangePassowrd(View):
	change_password_form = SetNewPasswordForm

	def get(self, request):
		change_password_form = self.change_password_form(self)
		return render(request, self.template, locals())

	def post(self, request):
		change_password_form = self.change_password_form(user = request.user, data = request.POST)
		if change_password_form.is_valid():
			change_password_form.save()
			messages.success(request, self.success_message)
			logout(request)
			return redirect(self.redirect_to)
		else:
			return self.get(request)


################# CRUD/LOGIN/LOGOUT AUTOR
class LoginAuthor(Login):
	login_form = LoginForm
	template = 'login_author.html'
	redirect_to = '/profile_author'

class LogoutAuthor(Logout):
	redirect_to = '/login_author'

class CreateAuthor(CreateUser):
	object_form = AuthorForm
	template = 'new_author.html'
	redirect_to = '/login_author'
	success_message = 'Autor cadastrado com sucesso!'

class EditAuthor(View):


	def post(self, request):
		author = Author.objects.get(user = request.user)
		if len(request.POST['first_name']) > 0:
			author.user.first_name = request.POST['first_name']
		if len(request.POST['last_name']) > 0:
			author.user.last_name = request.POST['last_name']
		if len(request.POST['email']) > 0:
			try:
				validate_email(request.POST['email'])
				author.user.email = request.POST['email']
			except:
				pass
		if len(request.POST['username']) > 0:
			author.user.username = request.POST['username']
		author.user.save()
		if len(request.POST['description']) > 0:
			author.description = request.POST['description']
		author.save()
		return redirect('/profile_author/')

class ChangePassowrdAuthor(ChangePassowrd):
	redirect_to = '/login_author'
	success_message = 'Senha alterada com sucesso!'
	template = 'change_password_author.html'

class ListAuthors(View):
	def get(self, request):
		qs_authors = Author.objects.all().order_by('user__first_name')
		return render(request, 'list_authors.html', locals())

class ViewAuthor(View):
	def get(self, request, id_author):
		author = Author.objects.get(id = id_author)
		return render(request, 'view_author.html', locals())

class ProfileAuthor(View):

	def get(self, request):
		author = Author.objects.get(user = request.user)
		qs_articles = Article.objects.filter(author = author)
		return render(request, 'profile_author.html', locals())

############## CRUD ARTIGO

class CreateArticle(View):

	def get(self, request):
		return render(request, 'new_article.html', locals())


	def post(self, request):
		if len(request.POST['content']) > 0:
			content = request.POST['content']
			title = request.POST['title']
			new_article = Article(title = title,
			content = content,
			author = Author.objects.get(user = request.user))
			new_article.save()
			return redirect('/profile_author/')
		else:
			return self.get(request)

class ListArticles(View):
	def get(self, request, id_author):
		qs_articles = Article.objects.filter(
		author__id = id_author).order_by('date_time')
		return render(request, 'list_articles.html', locals())

class ViewArticle(View):
	def get(self, request, id_article):
		article = Article.objects.get(id = id_article)
		return render(request, 'view_article.html', locals())

########## CRUD Leitor
class CreateReader(CreateUser):
	object_form = ReaderForm
	template = 'new_reader.html'
	redirect_to = '/login_reader'
	success_message = 'Conta criada com sucesso!'

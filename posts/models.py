# -*- coding: utf-8 -*-
import os
import datetime
from datetime import date
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
# Create your models here.

class Author(models.Model):
	user = models.OneToOneField(User)
	photo = models.ImageField(null = True, blank = True, upload_to = 'media/authors')
	description = models.TextField()

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

class Article(models.Model):
	author = models.ForeignKey(Author)
	title = models.CharField(max_length = 256, unique = True)
	content = models.TextField()
	date_time = models.DateTimeField(default = datetime.datetime.now())

	def __str__(self):
		return self.title

class Reader(models.Model):
	user = models.OneToOneField(User)
	photo = models.ImageField(null = True, blank = True, upload_to = 'media/readers')

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

class Comment(models.Model):
	author = models.ForeignKey(Reader)
	article = models.ForeignKey(Article)
	date_time = models.DateTimeField(default = datetime.datetime.now())
	content = models.TextField()

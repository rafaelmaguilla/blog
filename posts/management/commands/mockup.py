# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from posts.models import *
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date
from django.utils import timezone

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        somemodel_ct = ContentType.objects.get(app_label='auth', model='user')
        admin_group = Group(name='groupadmin')
        admin_group.save()
        author_group = Group(name='author_group')
        author_group.save()
        reader_group = Group(name='reader_group')
        reader_group.save()

        admin_perm = Permission(name='Admin Permission', codename='admin_perm',
                            content_type = somemodel_ct)
        admin_perm.save()
        author_perm = Permission(name='Author Permission', codename='author_perm',
                            content_type = somemodel_ct)
        author_perm.save()
        reader_perm = Permission(name='Reader Permission', codename='reader_perm',
                            content_type = somemodel_ct)
        reader_perm.save()

        for permission in Permission.objects.all():
            admin_group.permissions.add(permission)
        author_group.permissions.add(author_perm)
        reader_group.permissions.add(reader_perm)

        admin_user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        admin_user.groups.add(admin_group)

        def create_new_user(username, password, email, first_name, last_name):
            new_user = User(username = username,
                            password = password,
                            email = email,
                            first_name = first_name,
                            last_name = last_name)
            new_user.save()
            return new_user

        lira_user = create_new_user('lira', 'lira1', 'lira@lira.com', 'Thiago', 'Lira')
        maguilla_user = create_new_user('maguilla', 'maguilla1', 'maguilla@maguilla.com', 'Rafael', 'Maguilla')
        first_reader_user = create_new_user('reader1', 'reader1', 'reader@reader.com', 'Fulano', 'De Tal')
        second_reader_user = create_new_user('reader2', 'reader2', 'reader@reader.com', 'John', 'Doe')

        def create_new_author(user, description):
            new_author = Author(user = user,
                                description = description)
            new_author.save()
            return new_author

        lira_author = create_new_author(lira_user, 'MKSDSKDSKDSKDSKDSKDJSKDJSKDSKDJFJFKJDVKVIFAVNDFDIFJD')
        maguilla_author = create_new_author(maguilla_user, 'JDSIDJSIDJDIFJDIFJAVFJVBHBVFAFHUEHFUAFVHAUFHVUAFVH')

        def create_new_article(author, title, content):
            new_article = Article(author = author,
                                title = title,
                                content = content)
            new_article.save()
            return new_article

        lira_article = create_new_article(lira_author, 'Primeiro Artigo do Lira', 'Lorem Ipsum')
        maguilla_article = create_new_article(maguilla_author, 'Primeiro Artigo do Maguilla', 'Não concordo nem discordo, muito pelo contrário')

        def create_new_reader(user):
            new_reader = Reader(user = user)
            new_reader.save()
            return new_reader

        first_reader = create_new_reader(first_reader_user)
        second_reader = create_new_reader(second_reader_user)

        print('Mockup worked!')

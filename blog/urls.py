from django.conf.urls import include, url
from django.contrib import admin
from posts.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #AUTHORS' URLS
    url(r'^$', LoginAuthor.as_view()),
    url(r'^login_author/$', LoginAuthor.as_view()),
    url(r'^logout_author/$', LogoutAuthor.as_view()),
    url(r'^create_author/$', CreateAuthor.as_view()),
    url(r'^list_authors/$', ListAuthors.as_view()),
    url(r'^view_author/$', ViewAuthor.as_view()),
    url(r'^profile_author/$', ProfileAuthor.as_view()),
    url(r'^edit_author/$', EditAuthor.as_view()),
    url(r'^change_password_author/$', ChangePassowrdAuthor.as_view()),
    #ARTICLES' URLS
    url(r'^create_article/$', CreateArticle.as_view()),
    url(r'^list_articles/(?P<id_author>[0-9]+)/$', ListArticles.as_view()),
    url(r'^view_article/(?P<id_article>[0-9]+)/$', ViewArticle.as_view()),
    #READERS' URLS'
    url(r'^create_reader/$', CreateReader.as_view()),
]

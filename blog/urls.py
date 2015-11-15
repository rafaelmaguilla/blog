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
]

from django.conf.urls import patterns, include, url
from index import views as indexpage
from loginsystem import views as loginsystem
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GradeMate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', indexpage.index),
    url(r'^login/', loginsystem.login),
    url(r'^register/', loginsystem.register),
    url(r'^login2/', loginsystem.login2),
    url(r'^register2/', loginsystem.register2),
)

urlpatterns += staticfiles_urlpatterns()

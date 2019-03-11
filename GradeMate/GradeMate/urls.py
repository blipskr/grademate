from django.conf.urls import patterns, include, url
from mainsite import views as site
from loginsystem import views as loginsystem
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GradeMate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', site.index),
    url(r'^index.html', site.index),
    url(r'^login/', loginsystem.login_view),
    url(r'^register/', loginsystem.register_view),
)

urlpatterns += staticfiles_urlpatterns()

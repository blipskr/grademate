from django.conf.urls import patterns, include, url
from mainsite import views as site
from loginsystem import views as loginsystem
from game import views as game
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
    url(r'^logout/', loginsystem.logout_view),
    url(r'^profile/', loginsystem.profile_view),
    url(r'^agreement/', site.agreement),
    url(r'^creategame/', game.creategroup_view),
    url(r'^game/(?P<gamename>.+?)/managegame/$', game.managegroup_view),
    url(r'^game/(?P<gamename>.+?)/entermarks/$', game.entermarks_view),
    url(r'^joingame/', game.joingroup_view),
    url(r'^statistics/', loginsystem.statistics_view),
    url(r'^mygames/', site.mygroups),
    url(r'^accountsettings/', loginsystem.accountsettings_view),
    url(r'^game/(?P<gamename>.+?)/$', game.gamepage_view ),
    url(r'^test/', site.test),
)

urlpatterns += staticfiles_urlpatterns()

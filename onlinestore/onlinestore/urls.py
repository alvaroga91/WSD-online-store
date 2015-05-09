from django.conf.urls import patterns, include, url
from django.contrib import admin
from onlinestore.views import *

from onlinestore import views

urlpatterns = patterns('',
	url(r'^$', views.main),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/login'}),	
	url(r'^tweet/$', views.tweet),
	url(r'^registration/$', views.registration, name="register"),
	url(r'^games/add/$', views.addgame),
	url(r'^games/edit/$', views.editgame),
	url(r'^games/delete/$', views.deletegame),
	url(r'^games/sales/$', views.gamesales),
	url(r'^games/$', views.viewgames),
	url(r'^games/(?P<game_id>\d+)/$', views.viewgamepage),
	url(r'^profile/$', views.profile),
	
	url(r'^games/(?P<game_id>\d+)/play/$', views.playgamepage, name="play_game"),
	url(r'^games/(?P<game_id>\d+)/save/$', views.game_save),
	url(r'^games/(?P<game_id>\d+)/load/$', views.game_load),
	url(r'^games/(?P<game_id>\d+)/score/$', views.game_score),	
	url(r'^games/(?P<game_id>\d+)/buy/$', views.buygamepage),

	url(r'^payment/(?P<pid>\d+)/success', views.buysuccess),
	url(r'^payment/(?P<pid>\d+)/cancel', views.buycancel),	
	url(r'^payment/(?P<pid>\d+)/error', views.buyerror),	
	
)

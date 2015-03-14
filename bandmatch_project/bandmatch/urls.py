from django.conf.urls import patterns, url
from bandmatch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^your_bands/$', views.your_bands, name='your_bands'), # NEW MAPPING!
    url(r'^band/(?P<band_name_slug>[\w\-]+)/$', views.band, name='band'),
    url(r'^profile/(?P<band_name_slug>[\w\-]+)/add_band/$', views.add_band, name='add_band'),
    #url(r'^profile/$', views.profile, name='your_profile'), using the same url for your and other profiles
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[\w\-]+)', views.profile, name='profile'),
    url(r'^register/$', views.register_profile, name='register_profile'),
    url(r'^search_bands/', views.search_bands, name='search_bands'),
    url(r'^search_players/', views.search_players, name='search_players'),
    url(r'^logout/', views.user_logout, name='logout'),
      )
#    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
#    url(r'^login/$', views.user_login, name='login'),
    
#    url(r'^logout/$', views.user_logout, name='logout'),
# url(r'^search/',views.search,name = 'search'),
#
# url(r'^userlist/$', views.userlist, name='userlist'),
#    url(r'^like_category/$', views.like_category, name='like_category'),
#    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),

from django.conf.urls import patterns, url
from bandmatch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^your_bands/$', views.your_bands, name='your_bands'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^messages/$', views.display_messages, name='display_messages'),
    url(r'^messages/(?P<reciever>[\w\-]+)/(?P<title>[\w\-]+)/$', views.reply_message, name='reply_message'),
    url(r'^band/(?P<band_name_slug>[\w\-]+)/post_advert/$', views.post_advert, name='post_advert'),
    url(r'^band/(?P<band_name_slug>[\w\-]+)/display_advert/(?P<advert>\d+)/$', views.display_advert, name='display_advert'),    
    url(r'^band/(?P<band_name_slug>[\w\-]+)/$', views.band, name='band'),
    url(r'^band/(?P<band_name_slug>[\w\-]+)/edit/$', views.edit_band, name='edit_band'),
    url(r'^profile/add_band/$', views.add_band, name='make_a_band'),
    url(r'^profile/(?P<username>[\w\-]+)/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/change_password/$', views.change_password, name='change_password'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w\-]+)/add_to/$', views.add_player, name='add_player'),
    url(r'^register/$', views.register_profile, name='register_profile'),
    url(r'^search_bands/', views.search_bands, name='search_bands'),
    url(r'^search_players/', views.search_players, name='search_players'),
    url(r'^advanced_search/', views.advanced_search, name='advanced_search'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^suggest_username/$', views.suggest_username, name='suggest_username'),
    url(r'^suggest_member/(?P<band_name_slug>[\w\-]+)/$', views.suggest_member, name='suggest_member'),
    url(r'^suggest_band/$', views.suggest_band, name='suggest_band'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^delete_band/(?P<band_name_slug>[\w\-]+)$', views.delete_band, name='delete_band'),
    url(r'^delete_advert/(?P<advert_id>[\w\-]+)$', views.delete_advert, name='delete_advert'),
      )
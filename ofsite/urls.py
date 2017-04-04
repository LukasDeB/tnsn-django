from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.account_login, name='account_login'),
    url(r'^signup/$', views.account_signup, name='account_signup'),
    url(r'^logout/$', views.account_logout, name='account_logout'),
    url(r'^profile/(?P<username>.+)/$', views.profile, name='profile'),
    url(r'^post/(?P<post_id>[-\w]+)/$', views.view_post, name='view_post'),
    url(r'^post/(?P<post_id>[-\w]+)/comments', views.post_comments, name='post_comments'),
    url(r'^post/$', views.post, name='post'),

]

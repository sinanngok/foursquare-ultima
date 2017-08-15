from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.registration, name='registration'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^accounts/login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^ajax/add-to-favorites/$', views.add_to_favorites, name='add_to_favorites'),
    url(r'^ajax/remove-from-favorite-while-searching/$', views.remove_from_favorites_while_searching, name='remove_from_favorites_while_searching'),
    url(r'^favorites/$', views.favorites, name='favorites'),
    url(r'^remove-from-favorites/$', views.remove_from_favorites, name='remove_from_favorites'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]

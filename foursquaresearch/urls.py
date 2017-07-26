from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.registration, name='registration'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^add-to-favorites/$', views.add_to_favorites, name='add_to_favorites'),
    url(r'^history/$', views.user_search_history, name='user_search_history'),
    url(r'^favorites/$', views.favorites, name='favorites'),
    url(r'^remove-from-favorites/$', views.remove_from_favorites, name='remove_from_favorites'),


]

from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('draw/', views.drawer_view, name='draw'),
    path('guess/', views.guesser_view, name='guess'),
    path('play/', views.play_game, name='play_game'),
    # path('login/', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'web/login.html'}, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('api/word', views.word),
    path('api/<uuid:game_id>/finish', views.finish),
    path('api/<uuid:game_id>/record/path', views.record_stroke),
    path('api/<uuid:game_id>/record/word', views.record_word),
    path('api/<uuid:game_id>/record/chat', views.record_chat),
]
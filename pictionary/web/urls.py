from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('draw/', views.drawer_view, name='draw'),
    path('guess/', views.guesser_view, name='guess'),
    path('play/', views.play_game, name='play_game'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/word', views.word),
    path('api/<uuid:game_id>/finish', views.finish)
]
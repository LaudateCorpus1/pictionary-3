from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('draw/', views.drawer_view, name='draw'),
    path('guess/', views.guesser_view, name='guess'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout')
]
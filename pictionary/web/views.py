from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import Game

def login(request):
    return render(request, 'web/login.html', locals())

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def index(request):
    firstname = request.user.get_short_name()
    return render(request, 'web/index.html', locals())

@login_required
def drawer_view(request):
    user_id = request.user.id
    
    # Check for existing sessions of the user
    # If a session is found, ask for continuation/abandoning
    game = Game.objects.filter(Q(drawer=user_id) | Q(guesser=user_id))
    if game.count() != 0:
        game = game[0]
        return render(request, 'web/draw.html', locals())
    
    # Check for started session without a drawer
    # If not found, create a new session
    game = Game.objects.filter(wait_drawer=True).order_by('created_on')
    if game.count() != 0:
        game = game[0]
        game.wait_drawer = False
        game.drawer = user_id
        game.save(update_fields=['wait_drawer', 'drawer'])
    else:
        game = Game(drawer=user_id, wait_drawer=False)
        game.save()
    return render(request, 'web/draw.html', locals())

def tmp(request):
    game = Game(id=1)
    return render(request, 'web/draw.html', locals())

@login_required
def guesser_view(request):
    user_id = request.user.id
    
    # Check for existing sessions of the user
    # If a session is found, ask for continuation/abandoning
    game = Game.objects.filter(Q(drawer=user_id) | Q(guesser=user_id))
    if game.count() != 0:
        game = game[0]
        # if game.drawer == user_id:
        #     return render(request, 'web/draw.html', locals())
        return render(request, 'web/guess.html', locals())
    
    # Check for started session without a drawer
    # If not found, create a new session
    game = Game.objects.filter(wait_guesser=True).order_by('created_on')
    if game.count() != 0:
        game = game[0]
        game.wait_guesser = False
        game.guesser = user_id
        game.save(update_fields=['wait_guesser', 'guesser'])
    else:
        game = Game(guesser=user_id, wait_guesser=False)
        game.save()
    return render(request, 'web/guess.html', locals())
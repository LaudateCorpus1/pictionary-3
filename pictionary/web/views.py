from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import Game
from .models import Word
from .models import Path
from .models import Message
from .forms import PlayerDetailsForm
import random
import numpy as np
from django.utils import timezone
import pytz

def login(request):
    return render(request, 'web/login.html', locals())

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def register(request):
    if request.method == 'POST':
        form = PlayerDetailsForm(request.POST)
        if form.is_valid():
            user = request.user
            user.age = form.cleaned_data['age']
            user.hand = form.cleaned_data['hand']
            user.gender = form.cleaned_data['gender']
            user.save()
            return HttpResponseRedirect('/')
    form = PlayerDetailsForm()
    return render(request, 'registration/register.html', locals())

@login_required
def index(request):
    firstname = request.user.get_short_name()
    tutorial = False
    if not request.user.tutorial:
        if type(request.user.gender) == type(None):
            return HttpResponseRedirect('/register')
        tutorial = True
        request.user.tutorial = True
        request.user.save()
    return render(request, 'web/index.html', locals())

@login_required
def drawer_view(request):
    user_id = request.user.id
    
    # Check for existing sessions of the user
    # If a session is found, ask for continuation/abandoning
    game = Game.objects.filter(Q(drawer=user_id) | Q(guesser=user_id))
    if game.count() != 0:
        game = game[0]
        if game.guesser == user_id:
            return render(request, 'web/guess.html', locals())
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
        if game.drawer == user_id:
            return render(request, 'web/draw.html', locals())
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

@login_required
def play_game(request):
    user_id = request.user.id

    # Check for existing sessions of the user
    # If a session is found, ask for continuation/abandoning
    game = Game.objects.filter((Q(drawer=user_id) | Q(guesser=user_id)) & Q(abandoned=True))
    if game.count() != 0:
        game = game[0]
        if game.drawer == user_id:
            return render(request, 'web/draw.html', locals())
        return render(request, 'web/guess.html', locals())

    # Check for started session without a drawer
    # If not found, create a new session
    game = Game.objects.filter((Q(wait_drawer=True) & Q(abandoned=True))).order_by('created_on')
    if game.count() != 0:
        game = game[0]
        game.wait_drawer = False
        game.drawer = user_id
        game.save(update_fields=['wait_drawer', 'drawer'])
        return render(request, 'web/draw.html', locals())

    # Check for started session without a drawer
    # If not found, create a new session
    game = Game.objects.filter(Q(wait_guesser=True) & Q(abandoned=True)).order_by('created_on')
    if game.count() != 0:
        game = game[0]
        game.wait_guesser = False
        game.guesser = user_id
        game.save(update_fields=['wait_guesser', 'guesser'])
        return render(request, 'web/guess.html', locals())

    game = Game(drawer=user_id, wait_drawer=False)
    game.save()
    return render(request, 'web/draw.html', locals())

@login_required
def word(request):
    words = np.array(Word.objects.all())
    probs = []
    total = 0
    for word in words:
        probs.append(word.count)
        total += word.count
    if total == 0:
        probs = np.ones(words.shape)/len(words)
    else:
        probs = np.array(probs)/total
        probs = (1-probs)/probs.sum()
    word = np.random.choice(words, p=probs)
    return HttpResponse(word)

@login_required
def record_word(request, game_id):
    if request.method == 'POST':
        try:
            word = Word.objects.get(word=request.POST['word'])
            word.count += 1
            word.save()
        except Exception as e:
            return HttpResponse('failed')
        game = Game.objects.get(pk=game_id)
        game.word = request.POST['word']
        game.started_on = timezone.now()
        game.save()
        return HttpResponse('success')
    else:
        return HttpResponse('failed')

@login_required
def record_chat(request, game_id):
    if request.method == 'POST':    
        game = Game.objects.get(pk=game_id)
        msg = Message(
            message=request.POST['message'],
            game=game
        )
        msg.save()
        return HttpResponse('success')
    else:
        return HttpResponse('failed')

@login_required
def finish(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.abandoned = False
    game.ended_on = timezone.now()
    game.save()
    return HttpResponse('success')

@login_required
def record_stroke(request, game_id):
    if request.method == 'POST':
        game = Game.objects.get(pk=game_id)
        path = Path(
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            stroke=request.POST['path'],
            game=game
        )
        path.save()
        return HttpResponse('success')
    else:
        return HttpResponse('failed')
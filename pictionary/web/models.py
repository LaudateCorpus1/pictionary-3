import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model"""
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40, unique=True)
    tutorial = models.BooleanField(default=False)
    age = models.IntegerField(blank=True, null=True)
    hand = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    
    # USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drawer = models.IntegerField(blank=True, null=True)
    guesser = models.IntegerField(blank=True, null=True)
    wait_drawer = models.BooleanField(default=True)
    wait_guesser = models.BooleanField(default=True)
    word = models.TextField(blank=True, null=True)
    abandoned = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    started_on = models.DateTimeField(blank=True, null=True)
    ended_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} - {} vs {} - {}'.format(self.word, self.drawer, self.guesser, self.id)

class Path(models.Model):
    stroke = models.TextField()
    start_time = models.CharField(max_length=40)
    end_time = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.game.id) + ' - ' + self.stroke[:70]

class Message(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.game.id) + ' - ' + self.message

class Word(models.Model):
    word = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.word
        
import uuid
from django.db import models

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drawer = models.IntegerField(blank=True, null=True)
    guesser = models.IntegerField(blank=True, null=True)
    wait_drawer = models.BooleanField(default=True)
    wait_guesser = models.BooleanField(default=True)
    word = models.TextField(blank=True, null=True)
    abandoned = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} vs {} - {}'.format(self.word, self.drawer, self.guesser, self.id)

class Sketch(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(game.drawer, game.id)

class Path(models.Model):
    stroke = models.TextField()
    sketch = models.ForeignKey(Sketch, on_delete=models.CASCADE)

    def __str__(self):
        return stroke
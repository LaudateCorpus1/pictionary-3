from django.contrib import admin

from .models import Game, Path, Message, Word, User

class GameAdmin(admin.ModelAdmin):
    list_display = ('word', 'drawer', 'guesser', 'id', 'created_on')
    ordering = ('-created_on', '-started_on',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'age', 'hand', 'gender', 'last_login', 'is_staff', 'is_superuser')
    ordering = ('id',)

class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'count')
    ordering = ('-count', 'word',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('game', 'message', 'created_on')

admin.site.register(Game, GameAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Path)
admin.site.register(Word, WordAdmin)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from wordle.models import Wordle

class WordleAdmin(admin.ModelAdmin):
    list_filter = ('user', 'start_time')  # Assuming 'user' and 'start_time' are fields in your Wordle model

admin.site.register(Wordle, WordleAdmin)

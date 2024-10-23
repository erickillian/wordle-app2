from django.urls import path
from wordle.views import WordleViewSet, WordViewSet

from wordle import views

wordle_list = WordleViewSet.as_view({"get": "list"})
wordle_detail = WordleViewSet.as_view({"get": "retrieve"})

words_list = WordViewSet.as_view({"get": "list"})
words_detail = WordViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("status", views.WordleStatus.as_view()),
    path("guess", views.WordleGuess.as_view()),
    path("today", views.WordlesToday.as_view()),
    path("shame", views.WordleWallOfShame.as_view()),
    path("leaders/guesses", views.WordleLeadersGuesses.as_view()),
    path("leaders/time", views.WordleLeadersTime.as_view()),
    path("leaders/medals", views.WordleLeadersMedal.as_view()),
    path("stats", views.WordleStats.as_view()),
    path("wordles", wordle_list, name="wordle-list"),
    path("wordle/<slug:slug>", wordle_detail, name="wordle-detail"),
    path("user/<slug:slug>/wordles", views.UserWordleListView.as_view()),
    path("user/<slug:slug>/stats", views.UserWordleStatsView.as_view()),
    path("words", words_list, name="word-list"),
    path("words/<str:word>", words_detail, name="word-detail"),
    path("words/<str:word>/wordles", views.WordWordleListView.as_view()),
]

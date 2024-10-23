from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid

from wordle.constants import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES


User = get_user_model()


class Wordle(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    word = models.CharField(max_length=WORDLE_MAX_LENGTH, blank=False)
    guess_history = models.CharField(
        max_length=WORDLE_MAX_LENGTH * WORDLE_NUM_GUESSES, blank=True
    )
    guesses = models.PositiveSmallIntegerField(blank=False, default=1)
    start_time = models.DateTimeField(auto_now_add=True)
    time = models.DurationField(null=True, blank=True)
    active = models.BooleanField(default=True)
    solved = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=False, editable=False)

    @property
    def finished_time(self):
        if self.time:
            return self.start_time + self.time
        return self.start_time

    @property
    def date(self):
        return self.start_time.date()

    @property
    def correct(self):
        correct = ""
        for i in range(0, int(len(self.guess_history) / WORDLE_MAX_LENGTH)):
            guess = self.guess_history[
                i * WORDLE_MAX_LENGTH : (i + 1) * WORDLE_MAX_LENGTH
            ]
            word_copy = list(self.word)

            for j, letter in enumerate(guess):
                if letter == self.word[j]:
                    word_copy.pop(word_copy.index(letter))

            for j, letter in enumerate(guess):
                if letter == self.word[j]:
                    correct += "2"
                    if letter in word_copy:
                        word_copy.pop(word_copy.index(letter))
                elif letter in word_copy:
                    correct += "1"
                    word_copy.pop(word_copy.index(letter))
                else:
                    correct += "0"
        return correct

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super(Wordle, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.word} - active={self.active} - solved={self.solved}"

    class Meta:
        db_table = "wordle"
        verbose_name = _("Wordle")
        verbose_name_plural = _("Wordles")

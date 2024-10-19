from django.core.management.base import BaseCommand
from django.db import transaction

from django.contrib.auth import get_user_model
from faker import Faker
from django.utils import timezone
import datetime

import json, os, random

from wordle.constants import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES
from wordle.models import Wordle
User = get_user_model()

words = []
# Load target words from the JSON file in ../data/targetWords.json
with open(os.path.join(os.path.dirname(__file__), "../../data/targetWords.json"), "r") as file:
    words = list(json.load(file))


class Command(BaseCommand):
    help = "Creates some demo wordles for the users"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='The number of wordles to generate'
        )
        parser.add_argument(
            '--win-percentage',
            type=float,
            default=0.9,
            help='The win percentage for the wordles generated'
        )
        parser.add_argument(
            '--average-guesses',
            type=float,
            default=4,
            help='The average number of guesses for the wordles generated'
        )
        parser.add_argument(
            '--guesses-stddev',
            type=float,
            default=1,
            help='Guesses standard deviation'
        )

    def handle(self, *args, **options):
        count = options['count']
        win_percentage = options['win_percentage']
        average_guesses = options['average_guesses']
        guesses_stddev = options['guesses_stddev']
        self.stdout.write(self.style.SUCCESS(f"Creating {count} demo wordles with a win percentage of {win_percentage}."))

        with transaction.atomic():
            self.create_wordles(count, win_percentage, average_guesses, guesses_stddev)

        self.stdout.write(self.style.SUCCESS("Done."))

    def create_wordles(self, count, win_percentage, average_guesses, guesses_stddev):
        """Create some random wordles for the users"""
        self.stdout.write(self.style.SUCCESS("Creating random wordles..."))

        users = User.objects.all()

        for _ in range(count):
            solved = random.random() < win_percentage
            user = random.choice(users)
            word = random.choice(words)
            while True:
                start_time = timezone.now() - datetime.timedelta(days=random.randint(0, 20))
                time = datetime.timedelta(minutes=random.randint(1, 15), seconds=random.randint(0, 59), microseconds=random.randint(0, 999999))  # random time between 1 and 15 minutes with decimal component

                if not Wordle.objects.filter(start_time__date=start_time.date(), user=user).exists():
                    break
            
            if solved:
                guesses = max(1, min(WORDLE_NUM_GUESSES, round(random.normalvariate(average_guesses, guesses_stddev))))
                guess_history = "".join(
                    random.choices([w for w in words if w != word], k=guesses)
                )
                # replace the last guess with the word
                guess_history = guess_history[:-WORDLE_MAX_LENGTH] + word
            else:
                guesses = WORDLE_NUM_GUESSES
                guess_history = "".join(random.choices([w for w in words if w != word], k=guesses))
            wordle = Wordle(
                user=user,
                word=word,
                guess_history=guess_history,
                guesses=guesses,
                solved=solved,
                start_time=start_time,
                active=False,
                time=time,
            )
            wordle.save()
            wordle = Wordle.objects.get(id=wordle.id)
            wordle.start_time = start_time
            wordle.save()
            # Verify that the start_time was saved correctly
            saved_wordle = Wordle.objects.get(id=wordle.id)
            if saved_wordle.start_time != start_time:
                self.stdout.write(self.style.ERROR(f"Error: start_time for Wordle ID {wordle.id} was not saved correctly."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Wordle ID {wordle.id} created successfully with start_time {saved_wordle.start_time}."))


        return

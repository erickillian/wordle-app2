import datetime
import json
import os
import random

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Count, F, Q, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from rest_framework import generics, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.pagination import LargerResultsSetPagination, StandardResultsSetPagination
from backend.settings import BASE_DIR
from wordle.constants import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES
from wordle.models import Wordle
from wordle.serializers import *


wordle_target_words = json.load(
    open(os.path.join(BASE_DIR, "wordle/data/targetWords.json"))
)

User = get_user_model()


def add_wordle_rank_info(wordle):
    wordle.daily_rank = (
        Wordle.objects.filter(
            active=False,
            start_time__date=wordle.start_time.date(),  # Filter by the same day
        )
        .exclude(id=wordle.id)
        .filter(
            Q(guesses__lt=wordle.guesses) |
            (Q(guesses=wordle.guesses) & Q(time__lte=wordle.time))
        )
        .count()
        + 1
    )
    wordle.word_rank = (
        Wordle.objects.filter(
            active=False,
            word=wordle.word,  # Filter by the same day
        )
        .exclude(id=wordle.id)
        .filter(
            Q(guesses__lt=wordle.guesses)
            | (Q(guesses=wordle.guesses) & Q(time__lte=wordle.time))
        )
        .count()
        + 1
    )


class WordleStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wordle = Wordle.objects.filter(
                user=request.user, start_time__date=timezone.now().date()
            )
            if wordle.exists():
                wordle = wordle.first()
            else:
                raise Wordle.DoesNotExist
        except Wordle.DoesNotExist:
            print("No active Wordle game found.", flush=True)
            wordle = Wordle(
                word="?" * WORDLE_MAX_LENGTH,
                guess_history="",
                active=True,
                guesses=0,
                solved=False,
            )

        if wordle.active:
            serializer = ActiveWordleSerializer(wordle)
        else:
            add_wordle_rank_info(wordle)
            serializer = WordleSerializer(wordle)

        return Response(serializer.data)


class WordleGuess(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WordleGuessSerializer

    def post(self, request):
        wordle = self.get_today_wordle(request)
        if not wordle:
            return self.handle_new_wordle(request)

        if wordle.guesses >= WORDLE_NUM_GUESSES:
            return Response(
                {"error": "Maximum number of guesses reached."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not wordle.active or wordle.solved:
            return Response(
                {"error": "Wordle game for today has been completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.handle_existing_wordle(wordle, request)

    def serialize_wordle(self, wordle):
        if wordle.active:
            return ActiveWordleSerializer(wordle).data
        else:
            add_wordle_rank_info(wordle)
            return WordleSerializer(wordle).data

    def get_today_wordle(self, request):
        """Fetches today's Wordle game for the authenticated user."""
        return Wordle.objects.filter(
            user=request.user, start_time__date=timezone.now().date()
        ).first()

    def handle_new_wordle(self, request):
        """Handles creation of a new Wordle game."""
        guess_serializer = WordleGuessSerializer(data=request.data)
        if guess_serializer.is_valid():
            # Use a transaction to prevent double submissions from creating multiple Wordles
            with transaction.atomic():
                # Lock the Wordle row for this user on today's date
                wordle = (
                    Wordle.objects.select_for_update()
                    .filter(user=request.user, start_time__date=timezone.now().date())
                    .first()
                )

                # If Wordle exists after acquiring the lock, use it
                if wordle:
                    return self.handle_existing_wordle(wordle, request)

                # If Wordle does not exist, create a new one
                wordle = self.create_new_wordle(request)

            serializer = self.serialize_wordle(wordle)
            return Response(serializer, status=status.HTTP_201_CREATED)

        return Response(guess_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_new_wordle(self, request):
        """Creates a new Wordle game for the user."""
        word = random.choice(wordle_target_words)
        guess = request.data.get("guess", "")

        # Create a new Wordle instance
        wordle = Wordle.objects.create(
            user=request.user,
            word=word,
            guess_history=guess,
            guesses=1 if guess else 0,
            active=True,
            solved=False,
        )

        # Check if the first guess solves the Wordle
        if wordle.word == guess:
            wordle.solved = True
            wordle.active = False
            wordle.time = timezone.now() - wordle.start_time
            wordle.save()

        return wordle

    def handle_existing_wordle(self, wordle, request):
        """Handles updates to an existing Wordle game."""
        guess_serializer = self.serializer_class(data=request.data)
        if guess_serializer.is_valid():
            guess = request.data["guess"]

            # Check if the guess has already been made
            guess_history_list = [
                wordle.guess_history[i:i + WORDLE_MAX_LENGTH]
                for i in range(0, len(wordle.guess_history), WORDLE_MAX_LENGTH)
            ] if wordle.guess_history else []

            if guess in guess_history_list:
                return Response(
                    {"error": "You have already guessed this word."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the Wordle with the new guess
            wordle = self.update_wordle_with_guess(wordle, guess)
            serializer = self.serialize_wordle(wordle)
            return Response(serializer, status=status.HTTP_202_ACCEPTED)

        return Response(guess_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_wordle_with_guess(self, wordle, guess):
        """Updates the Wordle instance with the user's guess."""
        # Append the new guess to the guess history
        guess_history_list = (
            [
                wordle.guess_history[i : i + WORDLE_MAX_LENGTH]
                for i in range(0, len(wordle.guess_history), WORDLE_MAX_LENGTH)
            ]
            if wordle.guess_history
            else []
        )

        guess_history_list.append(guess)
        wordle.guess_history = "".join(guess_history_list)
        wordle.guesses = len(guess_history_list)
        wordle.save(update_fields=["guesses", "guess_history"])
        wordle.refresh_from_db()

        # Check if the new guess solves the Wordle
        if wordle.word == guess:
            wordle.solved = True
            wordle.active = False
            wordle.time = timezone.now() - wordle.start_time
            wordle.save(update_fields=["time", "active", "solved"])

        if wordle.guesses >= WORDLE_NUM_GUESSES or wordle.solved:
            wordle.active = False
            wordle.time = timezone.now() - wordle.start_time
            wordle.save(update_fields=["time", "active"])

        return wordle


class WordleViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for listing or retrieving Wordles.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer

    def get_queryset(self):
        return Wordle.objects.filter(active=False).order_by("guesses", "-time")

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)  # Paginate the queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        queryset = self.get_queryset()
        wordle = get_object_or_404(queryset, slug=slug)
        add_wordle_rank_info(wordle)
        serializer = self.get_serializer(wordle)
        return Response(serializer.data)

class UserWordleListView(generics.ListAPIView):
    """
    A view for listing Wordles for a specific user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = get_object_or_404(User, slug=self.kwargs["slug"])
        return Wordle.objects.filter(user=user, active=False).order_by("-start_time")


class UserWordleStatsView(APIView):
    """
    A view for getting statistics for a specific user include their guess distribution, average guesses, average time to solve
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)

        # Calculate average guesses
        guesses = Wordle.objects.filter(user=user, active=False).aggregate(Avg("guesses"))

        # Calculate total wordles
        total_wordles = Wordle.objects.filter(user=user, active=False).count()

        # Calculate average time to solve
        time = Wordle.objects.filter(user=user, active=False).aggregate(Avg("time"))

        # Calculate number of solved wordles
        solved_wordles = Wordle.objects.filter(user=user, active=False, solved=True).count()

        solved_percentage = (solved_wordles / total_wordles) * 100 if total_wordles > 0 else 0.0

        # Calculate guess distribution
        guess_distribution = (
            Wordle.objects.filter(user=user, active=False, solved=True)
            .values("guesses")
            .annotate(count=Count("guesses"))
            .order_by("guesses")
        )

        guess_distribution = {item["guesses"]: item["count"] for item in guess_distribution}
        guess_distribution = {i: guess_distribution.get(i, 0) for i in range(1, WORDLE_NUM_GUESSES + 1)}
        guess_distribution['Fails'] = Wordle.objects.filter(user=user, active=False, solved=False).count()

        user_data = UserSerializer(user).data

        response = {
            "user": user_data,
            "stats": {
                "avg_guesses": guesses["guesses__avg"],
                "total_wordles": total_wordles,
                "solved_percentage": solved_percentage,
                "avg_time": time["time__avg"],
                "guess_distribution": guess_distribution,
            },
        }
        return Response(response)


class WordleStats(APIView):
    """
    This view returns a bunch of Wordle stats
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = [
            self.total_wordles().data,
            self.most_wordles().data,
            self.wordle_avg_time().data,
            self.wordle_avg_guesses().data,
            self.best_word_wordle_guesses().data,
            self.best_profile_pic_average_guesses().data,
            self.best_profile_pic_average_time().data,
        ]
        return Response(stats)

    def total_wordles(self):
        total_wordles = Wordle.objects.filter(active=False, solved=True).count()
        return Response(
            {
                "stat_name": "Total Wordles Solved",
                "data": str(total_wordles),
            }
        )

    def wordle_avg_time(self):
        time = Wordle.objects.filter(active=False, solved=True).aggregate(Avg("time"))
        avg_time = time["time__avg"]
        formatted_time = str(datetime.timedelta(seconds=avg_time.total_seconds())) if avg_time else "N/A"
        return Response(
            {
            "stat_name": "Wordle Average Time",
            "data": formatted_time,
            }
        )

    def wordle_avg_guesses(self):
        guesses = Wordle.objects.filter(active=False, solved=True).aggregate(Avg("guesses"))
        return Response(
            {
                "stat_name": "Wordle Average Guesses",
                "data": str(guesses["guesses__avg"]),
            }
        )


    def best_word_wordle_guesses(self):
        # Group Wordles by 'word' and calculate the average guesses per word
        word_stats = (
            Wordle.objects.filter(active=False, solved=True)
            .values("word")
            .annotate(
                average_guesses=Avg("guesses")
            )
            .order_by("average_guesses")
            .first()
        )

        if word_stats:
            return Response(
                {
                    "stat_name": "Best Word Average Guesses",
                    "word": word_stats["word"],
                    "average_guesses": str(
                        word_stats["average_guesses"]
                    ),
                }
            )

        return Response(status=status.HTTP_404_NOT_FOUND)

    def most_wordles(self):
        user = User.objects.annotate(
            total_wordles=Count("wordle", filter=Q(wordle__active=False))
        ).order_by("-total_wordles").first()
        if user:
            return Response(
                {
                    "stat_name": "Most Wordles Solved",
                    "user": UserSerializer(user).data,
                    "data": str(user.total_wordles),
                }
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

    def best_profile_pic_average_guesses(self):
        user_profile_pics = (
            User.objects.filter(wordle__active=False)
            .values("profile_picture")
            .annotate(avg_guesses=Avg("wordle__guesses"))
            .order_by("avg_guesses")
        )

        if user_profile_pics.exists():
            best_profile_pic = user_profile_pics.first()
            profile_picture= best_profile_pic["profile_picture"]
            avg_guesses = best_profile_pic["avg_guesses"]
            return Response(
                {
                    "stat_name": "Best Average Guesses Animal",
                    "profile_picture": profile_picture,
                    "data": str(avg_guesses),
                }
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

    def best_profile_pic_average_time(self):
        user_profile_pics = (
            User.objects.filter(wordle__active=False)
            .values("profile_picture")
            .annotate(avg_time=Avg("wordle__time"))
            .order_by("avg_time")
        )

        if user_profile_pics.exists():
            best_profile_pic = user_profile_pics.first()
            profile_picture = best_profile_pic["profile_picture"]
            avg_time = best_profile_pic["avg_time"]
            return Response(
                {
                    "stat_name": "Best Average Time Animal",
                    "profile_picture": profile_picture,
                    "data": str(avg_time),
                }
            )
        return Response(status=status.HTTP_404_NOT_FOUND)


class WordlesToday(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer

    def get_queryset(self):
        queryset = Wordle.objects.filter(active=False, start_time__date=timezone.now().date()).order_by("-solved", "guesses", "time")
        return queryset

class WordleLeadersTime(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWordleSerializer

    def get(self, request):
        queryset = (
            User.objects.annotate(
                avg_time=Avg("wordle__time"), total_wordles=Count("wordle")
            )
            .filter(total_wordles__gte=10)
            .order_by("avg_time")[:5]
        )
        serializer = UserWordleSerializer(queryset, many=True)
        return Response(serializer.data)


class WordleLeadersGuesses(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWordleSerializer

    def get(self, request):
        queryset = (
            User.objects.annotate(
            avg_guesses=Avg("wordle__guesses", filter=Q(wordle__active=False)),
            total_wordles=Count("wordle", filter=Q(wordle__active=False))
            )
            .filter(total_wordles__gte=10)
            .order_by("avg_guesses")[:5]
        )
        serializer = UserWordleSerializer(queryset, many=True)
        return Response(serializer.data)


class WordleWallOfShame(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Wordle.objects.filter(solved=False, active=False).order_by("-time")


class WordleWallOfFame(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Wordle.objects.filter(solved=True, active=False, guesses=1)


# This view calculates the number of gold, silver, and bronze medals a user has
# It will also combine the medals into points, where gold = 3, silver = 2, and bronze = 1
# Users will be sorted by number of gold medals (no one cares about second place), then if there is a tie points will be used
# A gold medal is if you solved a wordle in the lowest number of guesses for that day, silver is second lowest, and bronze is third lowest. If there is a tie, time is used to break the tie
class WordleLeadersMedal(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(never_cache)
    def get(self, request):
        # Step 1: Annotate wordles with ranks and medals directly
        wordles_with_medals = Wordle.objects.filter(solved=True, active=False).annotate(
            rank=Window(
                expression=RowNumber(),
                partition_by=F("start_time__date"),
                order_by=[F("guesses").asc(), F("time").asc()],
            ),
        )

        # Step 2: Subquery for users' gold, silver, and bronze medals
        user_medals = User.objects.annotate(
            gold_medals=Count(
                "wordle", filter=Q(wordle__in=wordles_with_medals.filter(rank=1))
            ),
            silver_medals=Count(
                "wordle",
                filter=Q(wordle__in=wordles_with_medals.filter(rank=2)),
            ),
            bronze_medals=Count(
                "wordle",
                filter=Q(wordle__in=wordles_with_medals.filter(rank=3)),
            ),
            total_points=F("gold_medals") * 3
            + F("silver_medals") * 2
            + F("bronze_medals"),
        ).order_by("-gold_medals", "-total_points")[:5]

        return Response(UserWordleSerializer(user_medals, many=True).data)


class WordViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for listing or retrieving Words with their guess distribution.
    """
    # permission_classes = [IsAuthenticated]
    search_fields = ["word"]
    filter_backends = [SearchFilter]
    pagination_class = LargerResultsSetPagination

    def get_queryset(self):
        return Wordle.objects.values("word").annotate(
            total_wordles=Count("id"),
        ).order_by("word")

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)  # Paginate the queryset
        serializer = WordListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, word=None):
        queryset = Wordle.objects.filter(word=word).values("word").annotate(
            total_wordles=Count("id"),
        )
        wordle = get_object_or_404(queryset, word=word)

        # Calculate guess distribution
        guess_distribution = (
            Wordle.objects.filter(word=word, active=False, solved=True)
            .values("guesses")
            .annotate(count=Count("guesses"))
            .order_by("guesses")
        )

        guess_distribution = {item["guesses"]: item["count"] for item in guess_distribution}
        guess_distribution = {i: guess_distribution.get(i, 0) for i in range(1, WORDLE_NUM_GUESSES + 1)}
        guess_distribution['Fails'] = Wordle.objects.filter(word=word, active=False, solved=False).count()

        # Calculate average guesses
        guesses = Wordle.objects.filter(word=word, active=False).aggregate(Avg("guesses"))

        # Calculate total wordles
        total_wordles = Wordle.objects.filter(word=word, active=False).count()

        # Calculate average time to solve
        time = Wordle.objects.filter(word=word, active=False).aggregate(Avg("time"))

        # Calculate number of solved wordles
        solved_wordles = Wordle.objects.filter(word=word, active=False, solved=True).count()

        solved_percentage = (solved_wordles / total_wordles) * 100 if total_wordles > 0 else 0.0

        wordle_data = WordSerializer(wordle).data
        wordle_data["guess_distribution"] = guess_distribution
        wordle_data["stats"] = {
            "avg_guesses": guesses["guesses__avg"],
            "avg_time": time["time__avg"],
            "total_wordles": total_wordles,
            "solved_percentage": solved_percentage,
        }

        return Response(wordle_data)

class WordWordleListView(generics.ListAPIView):
    """
    A view for listing Wordles for a specific word.
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Wordle.objects.filter(word=self.kwargs["word"], active=False).order_by(
            "-solved", "guesses", "time", "start_time"
        )

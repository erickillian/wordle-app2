from rest_framework import serializers
from wordle.models import Wordle
from wordle.constants import WORDLE_NUM_GUESSES, WORDLE_MAX_LENGTH
import json, os
from backend.settings import BASE_DIR
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


valid_guess_words = json.load(
    open(os.path.join(BASE_DIR, "wordle/data/validGuessWords.json"))
)
word_definitions = json.load(
    open(os.path.join(BASE_DIR, "wordle/data/targetWordsDefinitions.json"))
)

def valid_guess(guess):
    if guess not in valid_guess_words:
        raise serializers.ValidationError("Guess not a valid word")


def valid_num_guesses(guesses):
    if guesses > WORDLE_NUM_GUESSES:
        raise serializers.ValidationError(
            "You have exceeded the number of allowed guesses"
        )

class WordleGuessSerializer(serializers.Serializer):
    guess = serializers.CharField(
        max_length=WORDLE_MAX_LENGTH, validators=[valid_guess]
    )


class ActiveWordleSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Wordle
        fields = [
            "slug",
            "start_time",
            "solved",
            "guess_history",
            "guesses",
            "correct",
            "time",
        ]


class WordleSerializer(ActiveWordleSerializer):
    user = UserSerializer()
    streak = serializers.IntegerField(read_only=True, required=False)
    definition = serializers.SerializerMethodField(method_name="get_definition", read_only=True, required=False)
    daily_rank = serializers.IntegerField(read_only=True, required=False)
    word_rank = serializers.IntegerField(read_only=True, required=False)

    def get_definition(self, obj):
        # Check if the serializer is being used in a list context
        if self.parent and isinstance(self.parent, serializers.ListSerializer):
            return None
        return word_definitions.get(obj.word, "")

    class Meta(ActiveWordleSerializer.Meta):
        model = Wordle
        fields = ActiveWordleSerializer.Meta.fields + [
            "user",
            "streak",
            "word",
            "definition",
            "daily_rank",
            "word_rank",
        ]


class UserWordleSerializer(serializers.ModelSerializer):
    avg_guesses = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    avg_time = serializers.DurationField(required=False)
    total_wordles = serializers.IntegerField(required=False)
    fails = serializers.IntegerField(required=False)
    gold_medals = serializers.IntegerField(read_only=True, required=False)
    silver_medals = serializers.IntegerField(read_only=True, required=False)
    bronze_medals = serializers.IntegerField(read_only=True, required=False)
    total_medals = serializers.IntegerField(read_only=True, required=False)
    total_points = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "display_name", 
            "profile_picture",
            "slug",
            "avg_guesses",
            "avg_time",
            "total_wordles",
            "fails",
            "gold_medals",
            "silver_medals",
            "bronze_medals",
            "total_medals",
            "total_points",
        ]
        read_only_fields = [
            "display_name",
            "profile_picture",
            "slug",
            "avg_guesses",
            "avg_time",
            "total_wordles",
            "fails",
            "gold_medals",
            "silver_medals",
            "bronze_medals",
            "total_medals",
            "total_points",
        ]


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wordle
        fields = ["word"]



class WordSerializer(serializers.ModelSerializer):
    definition = serializers.SerializerMethodField(method_name="get_definition", read_only=True)
    guess_distribution = serializers.JSONField(read_only=True, required=False)

    def get_definition(self, obj):
        print(obj, flush=True)
        return word_definitions.get(obj['word'], "")

    class Meta:
        model = Wordle
        fields = ["word", "definition", "guess_distribution"]
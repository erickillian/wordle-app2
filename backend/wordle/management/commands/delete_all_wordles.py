from django.core.management.base import BaseCommand
from wordle.models import Wordle

class Command(BaseCommand):
    help = 'Delete all Wordles'

    def handle(self, *args, **kwargs):
        Wordle.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all Wordles'))
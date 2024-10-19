from django.core.management.base import BaseCommand
from django.db import transaction

from django.contrib.auth import get_user_model
from faker import Faker
from concurrent.futures import ThreadPoolExecutor


User = get_user_model()


class Command(BaseCommand):
    help = "Creates some demo users for the django app"

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_users',
            type=int,
            default=10,
            help='The number of users to create'
        )

    def handle(self, *args, **options):
        num_users = options['num_users']
        print(f"Creating {num_users} demo users.")

        with transaction.atomic():
            self.create_users(num_users)

        print("Done.")

    def create_users(self, num_users):
        """Create some random users"""
        print("Creating random users...")

        fake = Faker()

        def create_single_user(_):
            full_name = fake.name()
            email = f"{full_name.replace(' ', '.').lower()}@example.com"
            new_user = User.objects.create(
                email=email,
                full_name=full_name,
            )
            new_user.set_password(fake.password())
            new_user.save()
            print(f"Created: {new_user.full_name}", flush=True)

        with ThreadPoolExecutor() as executor:
            executor.map(create_single_user, range(num_users))

        return

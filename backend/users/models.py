from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings
import uuid
import random
from rest_framework_simplejwt.tokens import OutstandingToken


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Ensure 'date_joined' is included here if referenced
    date_joined = models.DateTimeField(default=timezone.now)

    # User Properties
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True, default="")
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)

    # Light or dark mode or use system settings
    color_mode = models.CharField(
        max_length=10,
        choices=[("light", "Light"), ("dark", "Dark"), ("system", "System")],
        default="system",
    )

    PROFILE_PICTURES = [
        "bat.png",
        "bear.png",
        "beaver.png",
        "buffalo.png",
        "camel.png",
        "cat.png",
        "chameleon.png",
        "cheetah.png",
        "cow.png",
        "dog.png",
        "duck.png",
        "eagle.png",
        "elephant.png",
        "fox.png",
        "frog.png",
        "giraffe.png",
        "goat.png",
        "gorilla.png",
        "hamster.png",
        "hen.png",
        "hippo.png",
        "horse.png",
        "kangaroo.png",
        "koala.png",
        "lemur.png",
        "lion.png",
        "llama.png",
        "monkey.png",
        "ostrich.png",
        "owl.png",
        "panda-bear.png",
        "penguin.png",
        "pig.png",
        "polar-bear.png",
        "rabbit.png",
        "raccoon.png",
        "rhinoceros.png",
        "shark.png",
        "sheep.png",
        "sloth.png",
        "snake.png",
        "squirrel.png",
        "swan.png",
        "tiger.png",
        "turtle.png",
        "walrus.png",
        "wild-boar.png",
        "wolf.png",
        "zebra.png",
    ]

    profile_picture = models.CharField(
        max_length=15,
        choices=[(pic, pic.split(".")[0].capitalize()) for pic in PROFILE_PICTURES],
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def display_name(self):
        return self.full_name if self.full_name else self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())

        # Assign a random profile picture if one isn't already set
        if not self.profile_picture:
            self.profile_picture = random.choice(self.PROFILE_PICTURES)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name}"


class TokenMetadata(models.Model):
    token = models.OneToOneField(
        OutstandingToken, on_delete=models.CASCADE, related_name="metadata"
    )
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255, blank=True, null=False, default="Unknown Location")
    device = models.CharField(max_length=255, blank=True, null=False, default="Unknown Device")

    def __str__(self):
        return f"Token metadata: {self.ip_address} ({self.location})"


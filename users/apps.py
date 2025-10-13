from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import transaction
import os


def create_defaults(sender, **kwargs):
    from users.models import User

    try:
        with transaction.atomic():
            if not User.objects.filter(is_superuser=True).exists():
                username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
                email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@dass.com")
                password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "DassAdmin@123")

                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )

    except Exception as e:
        print("The Error comes while creating a SuperUser", str(e))
        pass


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        post_migrate.connect(create_defaults, sender=self)

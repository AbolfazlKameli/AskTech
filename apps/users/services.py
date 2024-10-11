from .models import User, UserProfile
from django.db import transaction


def create_user(*, username: str, email: str, password) -> User:
    return User.objects.create_user(username, email, password)


def create_user_profile(*, user: User) -> UserProfile:
    return UserProfile.objects.create(owner=user)


@transaction.atomic
def register(*, username: str, email: str, password: str) -> User:
    user = create_user(username=username, email=email, password=password)
    create_user_profile(user=user)
    return user

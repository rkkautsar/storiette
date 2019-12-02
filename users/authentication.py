import firebase_admin
from django.utils import timezone
from firebase_admin import auth as firebase_auth
from django.contrib.auth import get_user_model
from drf_firebase.authentication import BaseFirebaseAuthentication
from .models import FirebaseUser

User = get_user_model()
firebase_app = firebase_admin.initialize_app()


def create_django_user(user_record: firebase_auth.UserRecord):
    user = User.objects.create(
        username='_'.join(user_record.display_name.split(' ')),
        email=user_record.email,
        last_login=timezone.now(),
    )

    FirebaseUser.objects.create(
        user=user,
        uid=user_record.uid
    )

    user.profile.name = user_record.display_name
    user.profile.photo_url = user_record.photo_url
    user.profile.save()

    return user


class FirebaseAuthentication(BaseFirebaseAuthentication):
    keyword = 'Bearer'

    def get_firebase_app(self):
        return firebase_app

    def get_django_user(self, user_record: firebase_auth.UserRecord):
        email = user_record.email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = create_django_user(user_record)

        user.last_login = timezone.now()
        user.save()
        return user

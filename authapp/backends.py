from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from .models import UserUsername, UserPrimaryEmail

# Create your models here.


class EmailOrUsernameAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        if '@' in username:
            try:
                user_object = UserPrimaryEmail.objects.get(email=username)
            except UserPrimaryEmail.DoesNotExist:
                return 1
            user = user_object.user
            # user = User.objects.get(email=username)
            # kwargs = {'email': username}
        else:
            username = username.lower()
            try:
                user_object = UserUsername.objects.get(username=username)
            except UserUsername.DoesNotExist:
                return 2
            user = user_object.user
            # kwargs = {'username': username}
        try:
            # user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return 3

    def user_can_authenticate(self, user):
        return True
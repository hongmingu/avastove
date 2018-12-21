
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class UserUsername(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username = models.CharField(max_length=30, unique=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "UserUsername for %s" % self.user

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('baseapp:user_profile', kwargs={'user_username': self.username})


class UserBirthday(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "UserBrithday for %s" % self.user


STATUS_CHOICES = (
    (2, "female"),
    (1, "male"),
)


class UserGender(models.Model):

    gender = models.IntegerField(choices=STATUS_CHOICES, default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "UserGender for %s" % self.user


class UserTextName(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "UserName for %s" % self.user


class UserPrimaryEmail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_permitted = models.BooleanField(default=False)

    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "PrimaryEmail for %s" % self.user


class UserPrimaryEmailAuthToken(models.Model):
    user_primary_email = models.ForeignKey(UserPrimaryEmail, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=255)

    uid = models.CharField(max_length=64)
    token = models.CharField(max_length=34, unique=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        email = self.user_primary_email
        return "AuthToken for %s" % email


class UserPasswordResetToken(models.Model):
    user_primary_email = models.ForeignKey(UserPrimaryEmail, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=255)

    uid = models.CharField(max_length=64)
    token = models.CharField(max_length=34, unique=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user_primary_email is not None:
            email = self.user_primary_email
        else:
            email = "No email"
        return "PasswordAuthToken for %s" % email


class UserDelete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "UserDelete for %s" % self.user.userusername.username

import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    usernum =instance.user.username

    from django.utils.timezone import now
    now = now()
    now_date = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = "300_%s_%s.%s" % (now_date, uuid.uuid4(), ext)

    return os.path.join('photo/%s/userphoto' % usernum, filename)


def get_file_path_50(instance, filename):
    ext = filename.split('.')[-1]
    usernum = instance.user.username

    from django.utils.timezone import now
    now = now()
    now_date = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = "50_%s_%s.%s" % (now_date, uuid.uuid4(), ext)

    return os.path.join('photo/%s/userphoto' % usernum, filename)


class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    file_50 = models.ImageField(null=True, blank=True, default=None, upload_to=get_file_path)
    file_300 = models.ImageField(null=True, blank=True, default=None, upload_to=get_file_path_50)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "UserPhoto pk: %s, username: %s" % (self.pk, self.user.userusername.username)

    def file_50_url(self):
        if self.file_50:
            return self.file_50.url
        return settings.AWS_S3_SCHEME + settings.AWS_S3_CUSTOM_DOMAIN + "/media/default/default_photo_50.png"

    def file_300_url(self):
        if self.file_300:
            return self.file_300.url
        return settings.AWS_S3_SCHEME + settings.AWS_S3_CUSTOM_DOMAIN + "/media/default/default_photo_300.png"
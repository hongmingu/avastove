from urllib.request import urlopen

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from authapp.models import UserDelete
from django.utils.timezone import now, timedelta

class Command(BaseCommand):
    help = 'ping sitemaps on google or bing'

    def handle(self, *args, **options):
        User.objects.filter(userdelete__created__lte=now()-timedelta(days=14)).delete()



from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now, timedelta
import json
import urllib
from urllib.parse import urlparse
import ssl
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from post.models import Post
from post.models import PostEnglish

from dayemotion.models import DayEmotion
from daylove.models import DayLove
from daymoney.models import DayMoney
from dayrelationships.models import DayRelationships
from dayoverall.models import DayOverall
from daywork.models import DayWork
from website.utils import *
from django.core.cache import cache
from django.db.models import Q
from django.db.models.functions import Lower
from celebrity.utils import *
def test2(request):
    if request.method == "POST":
        pass
    else:
        # cache_data = cache.get_or_set('render', None)
        return render(request, 'website/main/test2.html')
# I hope the next gen of social media will allow a little bit more control over how we view our feeds.
# 6. Create Status Update Features
# 채팅방을 새로 만드는 게 아니라 유저목록(빈 대화 - 이렇게 빈 대화로 다 열어놔야 그룹열어도 어색하지않고 대화방이 이미 있는 상태라는 
# 설정이 도움이 될 것 같다) 위에 필요한 목록이 뜨는 형식으로.
def test(request):
    if request.method == "POST":
        pass
    else:
        # cache_data = cache.get_or_set('render', None)
        return render(request, 'website/main/test.html')
        # 각각 div 놓고 거기에 데이터까지 준 다음에 그걸로 따로 ajax 통신해서 각자 데이터 가져가게끔
        # if cache_data is None:
        #     rendered_data = render(request, 'website/main/test.html')
        #     cache.set('render', rendered_data)
        #     return rendered_data
        # else:
        #     return cache_data

        # get_data = request.GET.get('q', 'default_value')
        # get_cache = cache.get_or_set('posts'+get_data, get_data)
        #
        # answer = {'q': get_data}
        # return render(request, 'post/not_exist_post_default.html', {'answer': answer})


'''
class Post(models.Model):  
    ... # 생략
    def save(self, *args, **kwargs):
        cache.delete('posts')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('posts')
        super().delete(*args, **kwargs)

        # Good
entry.blog_id
# DB에 접속
e = Entry.objects.get(id=5)

# 관련된 Blog 객체를 가져오기 위해 DB에 한번 더 접속
b = e.blog

# select_related을 사용
# DB에 접속
e = Entry.objects.select_related('blog').get(id=5)

# 이미 위에서 관련된 Blog객체들을 가져왔기 때문에 DB에 접속하지 않음
b = e.blog
# Bad
entry.blog.id

# Good
my_band.members.add(me, my_friend)

# Bad
my_band.members.add(me)
my_band.members.add(my_friend)

render 값을 cache할 수 있는가?
'''

from django.db.models.signals import post_save, post_delete, pre_save
from post.models import *
from django.core.cache import cache
from django.dispatch import receiver

# 시그널 포함된 앱의 init에도 디펄트앱컨픽 넣어야하고

default_app_config = 'website.apps.WebsiteConfig'

# 시그널 포함된 앱의 앱스컨픽도 봐줘야함

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'website'

    def ready(self):
        import website.signals


@receiver(post_save, sender=Post)
def create_update_log(sender, instance, created, **kwargs):
    if created:
        PostArabic.objects.create(title='log2')
    else:
        PostArabic.objects.create(title='log2')


'''
def save(self, commit=True):
    user = super(CustomFormThing, self).save(commit=False)
    #set some other attrs on user here ...
    user._some = 'some'
    user._other = 'other'
    if commit:
        user.save()
    return user

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    some_id = getattr(instance, '_some', None)
    other_id = getattr(instance, '_other', None)
    if created:

'''


from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import PostCreateForm
from relation.models import *
from object.models import *
from object.numbers import *
from notice.models import *
from django.db.models import Q
from django.db import transaction
import uuid

from django.utils.timezone import now, timedelta

# Create your views here.

def user_profile(request, user_username):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = None
            try:
                chosen_user = User.objects.get(userusername__username=user_username)
            except:
                return render(request, '404.html')
            if chosen_user is not None:
                following = None
                if Follow.objects.filter(user=request.user, follow=chosen_user).exists():
                    following = True

                return render(request, 'baseapp/user_profile.html', {'chosen_user': chosen_user, 'following': following})
        else:
            user = None
            try:
                chosen_user = User.objects.get(userusername__username=user_username)
            except:
                return render(request, '404.html')
            if chosen_user is not None:
                following = None
                return render(request, 'baseapp/user_profile.html',
                              {'chosen_user': chosen_user, 'following': following})

def create_new(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostCreateForm(request.POST)
            if form.is_valid():
                title = None
                description = None
                # has_another_profile = False
                # profile_name = None
                open_close = False

                # if form.cleaned_data['whose'] == 'other':
                #     has_another_profile = True
                #     profile_name = form.cleaned_data['name']
                #     profile_name = profile_name.strip()
                title = None
                description = None
                if form.cleaned_data['open_close'] == 'open':
                    open_close = True

                uuid_made = uuid.uuid4().hex
                post = Post.objects.create(user=request.user,
                                           title=title,
                                           description=description,
                                           uuid=uuid_made,
                                           is_open=open_close)
                # if has_another_profile:
                #     PostProfile.objects.create(post=post, name=profile_name)
                post_like_count = PostLikeCount.objects.create(post=post)
                post_comment_count = PostCommentCount.objects.create(post=post)
                post_follow_count = PostFollowCount.objects.create(post=post)
                post_chat = PostChat.objects.create(post=post, before=None, kind=POSTCHAT_START, uuid=uuid.uuid4().hex)
                # post_chat_read = PostChatRead.objects.create(post=post_chat.post, post_chat=post_chat,
                #                                              user=request.user)
                post_read, created = PostRead.objects.get_or_create(post=post, user=request.user)
                post_read.post_chat_datetime = post_chat.created
                post_read.post_chat_uuid = post_chat.uuid
                post_read.save()
                # 여기서 post unique constraint 처리 해주면 좋긴 하나 지금 하기엔 하고 싶지 않다.
                return redirect(reverse('baseapp:post_update', kwargs={'uuid': uuid_made}))
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect(reverse('baseapp:main_create_log_in'))
        form = PostCreateForm
        return render(request, 'baseapp/create_new_first.html', {'form': form})


def post_update(request, uuid):
    if request.method == "GET":
        if request.user.is_authenticated:
            post = None
            try:
                post = Post.objects.get(uuid=uuid, user=request.user)

            except Post.DoesNotExist:
                return render(request, '404.html')

            return render(request, 'baseapp/post_update.html', {'post': post})

def post(request, uuid):
    if request.method == "GET":
        post = None
        try:
            post = Post.objects.get(uuid=uuid)
        except:
            return render(request, '404.html')
        if post is not None:
            id_data = {}
            id_data['id'] = uuid
            return render(request, 'baseapp/post.html', {'id_data': id_data, 'post': post})

        return render(request, 'baseapp/post.html', )


def explore_feed(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'baseapp/user_feed.html')
        else:
            return redirect(reverse('baseapp:main_create_log_in'))


def note_all(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                with transaction.atomic():
                    notices_update = Notice.objects.filter(Q(user=request.user) & Q(checked=False)).update(
                        checked=True)
                    notice_count = request.user.noticecount
                    notice_count.count = 0
                    notice_count.save()
            except Exception as e:
                print(e)
                pass
            return render(request, 'baseapp/user_note.html')
        else:
            return redirect(reverse('baseapp:main_create_log_in'))


def search_all(request):
    if request.method == "GET":
        q = request.GET.get('q', None)
        if q is None:
            q = ''
        q = q.strip()
        word = q
        return render(request, 'baseapp/user_search_all.html', {'word': word})

def search_user(request):
    if request.method == "GET":
        q = request.GET.get('q', None)
        if q is None:
            q = ''
        q = q.strip()
        word = q
        return render(request, 'baseapp/user_search_user.html', {'word': word})

def search_post(request):
    if request.method == "GET":
        q = request.GET.get('q', None)
        if q is None:
            q = ''
        q = q.strip()
        word = q
        return render(request, 'baseapp/user_search_post.html', {'word': word})
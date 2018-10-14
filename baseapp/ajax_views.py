import json
import urllib
from urllib.parse import urlparse

from PIL import Image
from io import BytesIO
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from authapp import options
from authapp import texts
from object.models import *
from .forms import PostProfilePhotoForm, PostChatPhotoForm
from relation.models import *
from notice.models import *
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.utils.html import escape, _js_escapes, normalize_newlines
from object.numbers import *


# Create your models here.
# 좋아요 비공개 할 수 있게
# 챗스톡, 페이지픽, 임플린, 챗카부 순으로 만들자.


@ensure_csrf_cookie
def re_create_new_upload_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            if request.is_ajax():
                try:
                    post = Post.objects.get(uuid=request.POST['post_id'])
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_profile = PostProfile.objects.get(post=post)
                except:
                    return JsonResponse({'res': 0})
                form = PostProfilePhotoForm(request.POST, request.FILES, instance=post_profile)
                if form.is_valid():

                    DJANGO_TYPE = request.FILES['file'].content_type

                    if DJANGO_TYPE == 'image/jpeg':
                        PIL_TYPE = 'jpeg'
                        FILE_EXTENSION = 'jpg'
                    elif DJANGO_TYPE == 'image/png':
                        PIL_TYPE = 'png'
                        FILE_EXTENSION = 'png'
                        # DJANGO_TYPE == 'image/gif
                    else:
                        return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})

                    from io import BytesIO
                    from PIL import Image
                    from django.core.files.uploadedfile import SimpleUploadedFile
                    import os
                    x = float(request.POST['x'])
                    y = float(request.POST['y'])
                    width = float(request.POST['width'])
                    height = float(request.POST['height'])
                    rotate = float(request.POST['rotate'])
                    # Open original photo which we want to thumbnail using PIL's Image
                    try:
                        with transaction.atomic():

                            image = Image.open(BytesIO(request.FILES['file'].read()))
                            image_modified = image.rotate(-1 * rotate, expand=True).crop((x, y, x + width, y + height))
                            # use our PIL Image object to create the thumbnail, which already
                            image = image_modified.resize((300, 300), Image.ANTIALIAS)

                            # Save the thumbnail
                            temp_handle = BytesIO()
                            image.save(temp_handle, PIL_TYPE, quality=90)
                            temp_handle.seek(0)

                            # Save image to a SimpleUploadedFile which can be saved into ImageField
                            # print(os.path.split(request.FILES['file'].name)[-1])
                            suf = SimpleUploadedFile(os.path.split(request.FILES['file'].name)[-1],
                                                     temp_handle.read(), content_type=DJANGO_TYPE)
                            # Save SimpleUploadedFile into image field
                            post_profile.file_300.save(
                                '%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                                suf, save=True)

                            # request.FILES['file'].seek(0)
                            # image = Image.open(BytesIO(request.FILES['file'].read()))

                            # use our PIL Image object to create the thumbnail, which already
                            image = image_modified.resize((50, 50), Image.ANTIALIAS)

                            # Save the thumbnail
                            temp_handle = BytesIO()
                            image.save(temp_handle, PIL_TYPE, quality=90)
                            temp_handle.seek(0)

                            # Save image to a SimpleUploadedFile which can be saved into ImageField
                            # print(os.path.split(request.FILES['file'].name)[-1])
                            suf = SimpleUploadedFile(os.path.split(request.FILES['file'].name)[-1],
                                                     temp_handle.read(), content_type=DJANGO_TYPE)
                            # Save SimpleUploadedFile into image field
                            # print(os.path.splitext(suf.name)[0])
                            # user_photo.file_50.save(
                            #     '50_%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                            #     suf, save=True)
                            post_profile.file_50.save(
                                '%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                                suf, save=True)
                            return JsonResponse({'res': 1, 'url': post_profile.file_300.url})
                    except Exception:
                        return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})

            return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})


# 이건 포스트의 프로필 이미지를 지우기 위함.
@ensure_csrf_cookie
def re_create_new_remove_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                if request.POST.get('command', None) == 'remove_photo':
                    post_id = request.POST.get('post_id', None)
                    try:
                        post = Post.objects.get(pk=post_id)
                    except:
                        return JsonResponse({'res': 0})
                    try:
                        post_profile = PostProfile.objects.get(post=post)
                    except:
                        return JsonResponse({'res': 0})
                    post_profile.file_50 = None
                    post_profile.file_300 = None
                    post_profile.save()
                    return JsonResponse({'res': 1})
                elif request.POST.get('whose', None) == 'other':
                    pass

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_create_new_text(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})

                try:
                    post_chat_last = PostChat.objects.filter(post=post).last()

                except PostChat.DoesNotExist:
                    return JsonResponse({'res': 0})

                you_say = False
                if request.POST.get('you_say', None) == 'you':
                    you_say = True
                post_chat = PostChat.objects.create(post=post, kind=POSTCHAT_TEXT, before=post_chat_last,
                                                    you_say=you_say, uuid=uuid.uuid4().hex)
                post_chat_text = PostChatText.objects.create(post_chat=post_chat, text=request.POST.get('text', None))
                return JsonResponse({'res': 1, 'content': post_chat.get_value()})

        return JsonResponse({'res': 2})


'''

@ensure_csrf_cookie
def re_create_new_text(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.last()
                except:
                    return JsonResponse({'res': 0})
                print('got post: ' + str(post))
                try:
                    post_chat_create = PostChat.objects.create(post=post, kind=POSTCHAT_TEXT, before=None, you_say=True, uuid=uuid.uuid4().hex)
                    print('post chat has been created')
                except Exception as e:
                    print('if it has exception: ' + str(e))
                print('just created post chat: ' + str(post_chat_create.pk))

                try:
                    post_chat_last = PostChat.objects.last()
                    print('any made post chat?: ' + str(post_chat_last.pk))

                except PostChat.DoesNotExist:
                    print('has error on getting post_chat_last')
                print('has no error on getting post_chat_last')
                you_say = False
                if request.POST.get('you_say', None) == 'you':
                    you_say = True
                print(request.POST.get('text', None))
                post_chat = PostChat.objects.create(kind=POSTCHAT_TEXT, before=post_chat_last, you_say=you_say, uuid=uuid.uuid4().hex)
                post_chat_text = PostChatText.objects.create(post_chat=post_chat, text=request.POST.get('text', None))
                return JsonResponse({'res': 1, 'content': post_chat.get_value()})

        return JsonResponse({'res': 2})'''


# 2018-07-28 해야 할 일: postchatphoto 업로드 테스트.


@ensure_csrf_cookie
def re_create_new_chat_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST['post_id']
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_chat_last = PostChat.objects.filter(post=post).last()
                except PostChat.DoesNotExist:
                    return JsonResponse({'res': 0})
                form = PostChatPhotoForm(request.POST, request.FILES)
                if form.is_valid():
                    you_say = True
                    if request.POST.get('you_say', None) == 'someone':
                        you_say = False
                    post_chat = PostChat.objects.create(kind=POSTCHAT_PHOTO, post=post, before=post_chat_last,
                                                        you_say=you_say, uuid=uuid.uuid4().hex)
                    post_chat_photo = PostChatPhoto.objects.create(post_chat=post_chat)

                    DJANGO_TYPE = request.FILES['file'].content_type

                    if DJANGO_TYPE == 'image/jpeg':
                        PIL_TYPE = 'jpeg'
                        FILE_EXTENSION = 'jpg'
                    elif DJANGO_TYPE == 'image/png':
                        PIL_TYPE = 'png'
                        FILE_EXTENSION = 'png'
                        # DJANGO_TYPE == 'image/gif
                    else:
                        return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})

                    from io import BytesIO
                    from PIL import Image
                    from django.core.files.uploadedfile import SimpleUploadedFile
                    import os
                    rotate = float(request.POST['rotate'])
                    # Open original photo which we want to thumbnail using PIL's Image

                    image = Image.open(BytesIO(request.FILES['file'].read()))
                    image = image.rotate(-1 * rotate, expand=True)
                    # use our PIL Image object to create the thumbnail, which already
                    # Save the thumbnail
                    temp_handle = BytesIO()
                    image.save(temp_handle, PIL_TYPE, quality=70)
                    temp_handle.seek(0)

                    # Save image to a SimpleUploadedFile which can be saved into ImageField
                    # print(os.path.split(request.FILES['file'].name)[-1])
                    suf = SimpleUploadedFile(os.path.split(request.FILES['file'].name)[-1],
                                             temp_handle.read(), content_type=DJANGO_TYPE)
                    # Save SimpleUploadedFile into image field
                    post_chat_photo.file.save(
                        '%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                        suf, save=True)

                    # request.FILES['file'].seek(0)
                    # image = Image.open(BytesIO(request.FILES['file'].read()))

                    # use our PIL Image object to create the thumbnail, which already
                    return JsonResponse({'res': 1, 'content': post_chat.get_value()})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_update(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)

                try:
                    post = Post.objects.get(uuid=post_id)
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})
                # 여기서 None 이 나오진 않고 기껏해야 빈 문자열이 오는 것이다.
                open = request.POST.get('open', None)
                title_command = request.POST.get('title_command', None)
                desc_command = request.POST.get('desc_command', None)
                title_add = None
                desc_add = None
                if open == 'open':
                    post.is_open = True
                elif open == 'close':
                    post.is_open = False
                if title_command == 'removed':
                    post.title = None
                elif title_command == 'add':
                    title_add = request.POST.get('title', None)
                    title_add = title_add.strip()
                    post.title = title_add
                if desc_command == 'removed':
                    post.description = None
                elif desc_command == 'add':
                    desc_add = request.POST.get('description', None)
                    desc_add = desc_add.strip()
                    post.description = desc_add
                post.save()
                return JsonResponse({'res': 1})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_update_profile_name(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                name = request.POST.get('name', None)
                name = name.strip()
                post = None
                try:
                    post = Post.objects.get(uuid=post_id)
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})
                if post is not None:
                    try:
                        post_profile = PostProfile.objects.get(post=post)
                    except Exception as e:
                        print(e)
                        return JsonResponse({'res': 0})
                    if post_profile is not None:
                        post_profile.name = name
                        post_profile.save()

                return JsonResponse({'res': 1})

        return JsonResponse({'res': 2})
@ensure_csrf_cookie
def re_post_chat_remove(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat.delete()
                return JsonResponse({'res': 1})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_modify_populate(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat_set = post.postchat_set.all().order_by('-created')[:20]
                from django.core import serializers
                post_chat_set = serializers.serialize('python', post_chat_set)
                actual_data = [PostChat.objects.get(pk=item['pk']).get_value() for item in post_chat_set]
                output = json.dumps(actual_data)
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_more_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                post_chat_id = request.POST.get('post_chat_id', None)

                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                from django.db.models import Q
                standard_post_chat = PostChat.objects.get(uuid=post_chat_id)
                post_chat_set = PostChat.objects.filter(
                    Q(post=post) & Q(created__lt=standard_post_chat.created)).order_by('-created')[:10]
                from django.core import serializers
                post_chat_set = serializers.serialize('python', post_chat_set)
                actual_data = [PostChat.objects.get(pk=item['pk']).get_value() for item in post_chat_set]
                output = json.dumps(actual_data)
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_home_feed(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                last_id = request.POST.get('last_id', None)
                posts = None
                if last_id == '':
                    posts = Post.objects.filter(
                        (Q(user__is_followed__user=request.user) | Q(post_follow__user=request.user)) & Q(
                            is_open=True)).order_by('-post_chat_created').distinct()[:30]
                else:
                    last_post = None
                    try:
                        last_post = Post.objects.get(uuid=last_id)
                    except Exception as e:
                        print(e)
                        return JsonResponse({'res': 0})

                    posts = Post.objects.filter(
                        (Q(user__is_followed__user=request.user) | Q(post_follow__user=request.user)) & Q(
                            is_open=True) & Q(post_chat_created__lte=last_post.post_chat_created)).exclude(pk=last_post.pk).order_by('-post_chat_created').distinct()[:30]

                ################################
                output = []
                count = 0
                last = None
                post_follow = None
                for post in posts:
                    count = count + 1
                    if count == 30:
                        last = post.uuid
                    post_follow = True
                    if Follow.objects.filter(user=request.user, follow=post.user).exists():
                        post_follow = False
                    sub_output = {
                        'id': post.uuid,
                        'created': post.created,
                        'post_follow': post_follow
                    }

                    output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'last': last})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_comment_add(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                text = request.POST.get('comment', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                    # post = Post.objects.last()

                except:
                    return JsonResponse({'res': 0})
                try:
                    with transaction.atomic():
                        post_comment = PostComment.objects.create(post=post, user=request.user, uuid=uuid.uuid4().hex,
                                                                  text=text)
                        from django.db.models import F
                        post_comment_count = post.postcommentcount
                        post_comment_count.count = F('count') + 1
                        post_comment_count.save()
                        # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                except Exception:
                    return JsonResponse({'res': 0})

                output = []
                sub_output = {}
                if post_comment is not None:
                    sub_output = {
                            'comment_user_id': post_comment.user.username,
                            'comment_username': post_comment.user.userusername.username,
                            'comment_text': escape(post_comment.text),
                            'comment_created': post_comment.created,
                            'comment_uuid': post_comment.uuid,
                        }
                output.append(sub_output)
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_comment_delete(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                comment_id = request.POST.get('comment_id', None)
                post_id = request.POST.get('post_id', None)
                try:
                    # post = Post.objects.last()
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})

                try:
                    comment = PostComment.objects.get(uuid=comment_id, user=request.user)
                except:
                    try:
                        comment = PostComment.objects.get(uuid=comment_id, post=post, post__user=request.user)
                    except:
                        return JsonResponse({'res': 0})

                try:
                    with transaction.atomic():
                        comment.delete()
                        from django.db.models import F
                        post_comment_count = post.postcommentcount
                        post_comment_count.count = F('count') - 1
                        post_comment_count.save()
                except Exception:
                    return JsonResponse({'res': 0})
                return JsonResponse({'res': 1})
        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_comment_more_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                last_comment_id = request.POST.get('last_comment_id', None)

                try:
                    post = Post.objects.get(uuid=post_id)
                except Exception:
                    return JsonResponse({'res': 0})

                post_comment_last = PostComment.objects.get(uuid=last_comment_id)

                post_comments = PostComment.objects.filter(Q(post=post) & Q(created__gt=post_comment_last.created)).order_by('created')[:20]

                post_comment_uuids = [post_comment.uuid for post_comment in post_comments]
                output = []

                post_comment_end = PostComment.objects.last()
                post_comment = None
                end = False
                if post_comments:
                    for item in post_comment_uuids:
                        try:
                            post_comment = PostComment.objects.get(uuid=item)
                        except:
                            pass
                        if post_comment is not None:
                            sub_output = {
                                'comment_user_id': post_comment.user.username,
                                'comment_username': post_comment.user.userusername.username,
                                'comment_text': escape(post_comment.text),
                                'comment_created': post_comment.created,
                                'comment_uuid': post_comment.uuid,
                            }
                            output.append(sub_output)
                            if post_comment.uuid == post_comment_end.uuid:
                                end = True
                else:
                    output = None
                    end = True
                return JsonResponse({'res': 1, 'set': output, 'end': end})
        else:
            post_id = request.POST.get('post_id', None)
            last_comment_id = request.POST.get('last_comment_id', None)

            try:
                post = Post.objects.get(uuid=post_id)
            except Exception:
                return JsonResponse({'res': 0})

            post_comment_last = PostComment.objects.get(uuid=last_comment_id)

            post_comments = PostComment.objects.filter(
                Q(post=post) & Q(created__gt=post_comment_last.created)).order_by('created')[:20]

            post_comment_uuids = [post_comment.uuid for post_comment in post_comments]
            output = []

            post_comment_end = PostComment.objects.last()
            post_comment = None
            end = False
            if post_comments:
                for item in post_comment_uuids:
                    try:
                        post_comment = PostComment.objects.get(uuid=item)
                    except:
                        pass
                    if post_comment is not None:
                        sub_output = {
                            'comment_user_id': post_comment.user.username,
                            'comment_username': post_comment.user.userusername.username,
                            'comment_text': escape(post_comment.text),
                            'comment_created': post_comment.created,
                            'comment_uuid': post_comment.uuid,
                        }
                        output.append(sub_output)
                        if post_comment.uuid == post_comment_end.uuid:
                            end = True
            else:
                output = None
                end = True
            return JsonResponse({'res': 1, 'set': output, 'end': end})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_like(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    # post = Post.objects.last()
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_like = PostLike.objects.get(post=post, user=request.user)
                except PostLike.DoesNotExist:
                    post_like = None

                liked = None
                if post_like is not None:
                    try:
                        with transaction.atomic():
                            post_like.delete()
                            from django.db.models import F
                            post_like_count = post.postlikecount
                            post_like_count.count = F('count') - 1
                            post_like_count.save()
                            liked = False
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})
                else:
                    try:
                        with transaction.atomic():
                            post_like = PostLike.objects.create(post=post, user=request.user)
                            from django.db.models import F
                            post_like_count = post.postlikecount
                            post_like_count.count = F('count') + 1
                            post_like_count.save()
                            liked = True
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'liked': liked})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_user_home_populate(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                from django.db.models import Q
                name = post.user.usertextname.name
                profile_photo = post.user.userphoto.file_50_url()

                if post.has_another_profile:
                    name = post.postprofile.name
                    profile_photo = post.postprofile.file_50_url()
                you_liked = False
                if PostLike.objects.filter(user=request.user, post=post).exists():
                    you_liked = True
                post_chat_read = PostChatRead.objects.filter(post=post, user=request.user).last()
                post_chat = None
                post_chat_last_chat = None
                if post_chat_read is None:
                    try:
                        post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                    except IndexError:
                        post_chat_last_chat = {'kind': 'start'}
                    if post_chat is not None:
                        if post_chat.kind == POSTCHAT_TEXT:
                            post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                    'text': escape(post_chat.postchattext.text)}
                        elif post_chat.kind == POSTCHAT_PHOTO:
                            post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}
                else:
                    if post_chat_read.post_chat.kind == POSTCHAT_START:
                        try:
                            post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                        except IndexError:
                            post_chat_last_chat = {'kind': 'start'}
                        if post_chat is not None:
                            if post_chat.kind == POSTCHAT_TEXT:
                                post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                                  'text': escape(post_chat.postchattext.text)}
                            elif post_chat.kind == POSTCHAT_PHOTO:
                                post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say,
                                                  'url': post_chat.postchatphoto.file.url}
                    elif post_chat_read.post_chat.kind == POSTCHAT_TEXT:
                        post_chat = post_chat_read.post_chat
                        post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say, 'text': escape(post_chat.postchattext.text)}
                    elif post_chat_read.post_chat.kind == POSTCHAT_PHOTO:
                        post_chat = post_chat_read.post_chat
                        post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}

                new = True
                post_chat_last = PostChat.objects.filter(post=post).last()
                post_chat_read_last = PostChatRead.objects.filter(post=post, user=request.user).last()
                if post_chat_read_last is not None:
                    if post_chat_read_last.post_chat == post_chat_last:
                        new = False
                    else:
                        new = True

                user_follow = False
                if Follow.objects.filter(user=request.user, follow=post.user).exists():
                    user_follow = True

                post_follow = False
                if PostFollow.objects.filter(post=post, user=request.user).exists():
                    post_follow = True

                output = {'title': post.title,
                          'desc': post.description,
                          'username': post.user.userusername.username,
                          'user_id': post.user.username,
                          'name': name,
                          'photo': profile_photo,
                          'created': post.post_chat_created,
                          'last_chat': post_chat_last_chat,
                          'absolute_url': post.get_absolute_url(),
                          'id': post.uuid,
                          'like_count': post.postlikecount.count,
                          'you_liked': you_liked,
                          'comment_count': post.postcommentcount.count,
                          'three_comments': post.get_three_comments(),
                          'new': new,
                          'user_follow': user_follow,
                          'post_follow': post_follow,
                          'post_follow_count': post.postfollowcount.count,
                          }
                return JsonResponse({'res': 1, 'set': output})
        else:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                from django.db.models import Q
                name = post.user.usertextname.name
                profile_photo = post.user.userphoto.file_50_url()

                if post.has_another_profile:
                    name = post.postprofile.name
                    profile_photo = post.postprofile.file_50_url()
                you_liked = False
                post_chat_read = None
                post_chat = None
                post_chat_last_chat = None
                if post_chat_read is None:
                    try:
                        post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                    except IndexError:
                        post_chat_last_chat = {'kind': 'start'}
                    if post_chat is not None:
                        if post_chat.kind == POSTCHAT_TEXT:
                            post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                    'text': escape(post_chat.postchattext.text)}
                        elif post_chat.kind == POSTCHAT_PHOTO:
                            post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}

                new = True

                user_follow = False

                post_follow = False

                output = {'title': post.title,
                          'desc': post.description,
                          'username': post.user.userusername.username,
                          'user_id': post.user.username,
                          'name': name,
                          'photo': profile_photo,
                          'created': post.created,
                          'last_chat': post_chat_last_chat,
                          'absolute_url': post.get_absolute_url(),
                          'id': post.uuid,
                          'like_count': post.postlikecount.count,
                          'you_liked': you_liked,
                          'comment_count': post.postcommentcount.count,
                          'three_comments': post.get_three_comments(),
                          'new': new,
                          'user_follow': user_follow,
                          'post_follow': post_follow,
                          'post_follow_count': post.postfollowcount.count,
                          }
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_already_read(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    # post = Post.objects.last()
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})

                try:
                    post_chat_reads = PostChatRead.objects.filter(post_chat__post=post, user=request.user).order_by('-created')[:20]
                except:
                    return JsonResponse({'res': 0})

                post_chats = [post_chat_read.post_chat for post_chat_read in post_chat_reads]
                output = []
                last_post_chat = None
                if post_chats:
                    first_check = True
                    for post_chat in post_chats:
                        try:
                            count = post_chat.postchatlikecount.count
                        except:
                            count = None
                        # 여기서 you_like 부터 시작해야한다.
                        you_like = False
                        if PostChatLike.objects.filter(user=request.user, post_chat=post_chat).exists():
                            you_like = True
                        sub_output = {
                            'id': post_chat.uuid,
                            'kind': post_chat_kind_converter(post_chat.kind),
                            'like_count': count,
                            'created': post_chat.created,
                            'you_say': post_chat.you_say,
                            'content': post_chat.get_raw_value(),
                            'rest_count': post_chat.postchatrestmessagecount.count,
                            'you_like': you_like
                        }

                        output.append(sub_output)

                        if first_check is True:
                            last_post_chat = post_chat
                        first_check = False

                else:
                    post_chats = PostChat.objects.filter(post=post).order_by('created')[:2]
                    for post_chat in post_chats:

                        try:
                            count = post_chat.postchatlikecount.count
                        except:
                            count = None
                        you_like = False
                        if PostChatLike.objects.filter(user=request.user, post_chat=post_chat).exists():
                            you_like = True
                        sub_output = {
                            'id': post_chat.uuid,
                            'kind': post_chat_kind_converter(post_chat.kind),
                            'like_count': count,
                            'created': post_chat.created,
                            'you_say': post_chat.you_say,
                            'content': post_chat.get_raw_value(),
                            'rest_count': post_chat.postchatrestmessagecount.count,
                            'you_like': you_like
                        }

                        output.insert(0, sub_output)

                        post_chat_read = PostChatRead.objects.create(post=post, post_chat=post_chat, user=request.user)
                        last_post_chat = post_chat

                next = None
                if last_post_chat is not None:

                    try:
                        post_chat_next = PostChat.objects.get(before=last_post_chat)
                    except PostChat.DoesNotExist:
                        post_chat_next = None
                    if post_chat_next is not None:
                        next = {
                            'kind': post_chat_kind_converter(post_chat_next.kind),
                            'content': post_chat_next.get_value(),
                        }

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        else:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    # post = Post.objects.last()
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                output = []
                post_chats = PostChat.objects.filter(post=post).order_by('created')[:2]

                last_post_chat = None
                for post_chat in post_chats:

                    try:
                        count = post_chat.postchatlikecount.count
                    except:
                        count = None
                    you_like = False
                    sub_output = {
                        'id': post_chat.uuid,
                        'kind': post_chat_kind_converter(post_chat.kind),
                        'like_count': count,
                        'created': post_chat.created,
                        'you_say': post_chat.you_say,
                        'content': post_chat.get_raw_value(),
                        'rest_count': post_chat.postchatrestmessagecount.count,
                        'you_like': you_like
                    }

                    output.insert(0, sub_output)

                    last_post_chat = post_chat

                next = None
                if last_post_chat is not None:

                    try:
                        post_chat_next = PostChat.objects.get(before=last_post_chat)
                    except PostChat.DoesNotExist:
                        post_chat_next = None
                    if post_chat_next is not None:
                        next = {
                            'kind': post_chat_kind_converter(post_chat_next.kind),
                            'content': post_chat_next.get_value(),
                        }

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_reading_more_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                last_id = request.POST.get('post_chat_before_id', None)
                post_id = request.POST.get('post_id', None)
                try:
                    last_post_chat = PostChat.objects.get(uuid=last_id)
                except:
                    return JsonResponse({'res': 0})

                post_chats = PostChat.objects.filter(Q(post__uuid=post_id) & Q(pk__lt=last_post_chat.pk)).order_by('-created')[:11]

                output = []
                if post_chats:
                    for post_chat in post_chats:
                        try:
                            count = post_chat.postchatlikecount.count
                        except:
                            count = None
                        # 여기서 you_like 부터 시작해야한다.
                        you_like = False
                        if PostChatLike.objects.filter(user=request.user, post_chat=post_chat).exists():
                            you_like = True
                        sub_output = {
                            'id': post_chat.uuid,
                            'kind': post_chat_kind_converter(post_chat.kind),
                            'like_count': count,
                            'created': post_chat.created,
                            'you_say': post_chat.you_say,
                            'content': post_chat.get_raw_value(),
                            'rest_count': post_chat.postchatrestmessagecount.count,
                            'you_like': you_like
                        }

                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output})
        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_next_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_next_id', None)
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                output = []
                next = None
                if post_chat is not None:
                    try:
                        count = post_chat.postchatlikecount.count
                    except:
                        count = None
                    you_like = False
                    if PostChatLike.objects.filter(user=request.user, post_chat=post_chat).exists():
                        you_like = True
                    sub_output = {
                        'id': post_chat.uuid,
                        'kind': post_chat_kind_converter(post_chat.kind),
                        'like_count': count,
                        'created': post_chat.created,
                        'you_say': post_chat.you_say,
                        'content': post_chat.get_raw_value(),
                        'rest_count': post_chat.postchatrestmessagecount.count,
                        'you_like': you_like
                    }
                    post_chat_read = PostChatRead.objects.create(post=post_chat.post, post_chat=post_chat, user=request.user)

                    output.append(sub_output)
                    try:
                        post_chat_next = PostChat.objects.get(before=post_chat)
                    except PostChat.DoesNotExist:
                        post_chat_next = None
                    if post_chat_next is not None:
                        next = {
                            'kind': post_chat_kind_converter(post_chat_next.kind),
                            'content': post_chat_next.get_value(),
                        }

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        else:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_next_id', None)
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                output = []
                next = None
                if post_chat is not None:
                    try:
                        count = post_chat.postchatlikecount.count
                    except:
                        count = None
                    you_like = False
                    sub_output = {
                        'id': post_chat.uuid,
                        'kind': post_chat_kind_converter(post_chat.kind),
                        'like_count': count,
                        'created': post_chat.created,
                        'you_say': post_chat.you_say,
                        'content': post_chat.get_raw_value(),
                        'rest_count': post_chat.postchatrestmessagecount.count,
                        'you_like': you_like
                    }

                    output.append(sub_output)
                    try:
                        post_chat_next = PostChat.objects.get(before=post_chat)
                    except PostChat.DoesNotExist:
                        post_chat_next = None
                    if post_chat_next is not None:
                        next = {
                            'kind': post_chat_kind_converter(post_chat_next.kind),
                            'content': post_chat_next.get_value(),
                        }

                return JsonResponse({'res': 1, 'set': output, 'next': next})
        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_like(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except PostChat.DoesNotExist as e:
                    print(e)
                    return JsonResponse({'res': 0})
                try:
                    post_chat_like = PostChatLike.objects.get(post_chat=post_chat, user=request.user)
                except PostChatLike.DoesNotExist:
                    post_chat_like = None

                liked = None
                if post_chat_like is not None:
                    try:
                        with transaction.atomic():
                            post_chat_like.delete()
                            from django.db.models import F
                            post_chat_like_count = post_chat.postchatlikecount
                            post_chat_like_count.count = F('count') - 1
                            post_chat_like_count.save()
                            liked = False
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception as e:
                        print(e)
                        return JsonResponse({'res': 0})
                else:
                    try:
                        with transaction.atomic():
                            post_chat_like = PostChatLike.objects.create(post_chat=post_chat, user=request.user)
                            from django.db.models import F
                            post_chat_like_count = post_chat.postchatlikecount
                            post_chat_like_count.count = F('count') + 1
                            post_chat_like_count.save()
                            liked = True
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception as e:
                        print(e)
                        return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'liked': liked})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_add_rest(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                text = request.POST.get('text', None)
                post_chat = None
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat_rest_message = None
                sub_output = None
                if post_chat is not None:
                    post_chat_rest_message = PostChatRestMessage.objects.create(text=text, user=request.user, uuid=uuid.uuid4().hex, post_chat=post_chat)

                    from django.db.models import F
                    post_chat_rest_message_count = post_chat.postchatrestmessagecount
                    post_chat_rest_message_count.count = F('count') + 1
                    post_chat_rest_message_count.save()

                if post_chat_rest_message is not None:
                    sub_output = {
                        'id': post_chat_rest_message.uuid,
                        'name': post_chat_rest_message.user.usertextname.name,
                        'user_id': post_chat_rest_message.user.username,
                        'created': post_chat_rest_message.created,
                        'text': post_chat_rest_message.text,
                        'photo': post_chat_rest_message.user.userphoto.file_50_url()
                    }
                return JsonResponse({'res': 1, 'set': sub_output})
        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_chat_rest_more_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                last_id = request.POST.get('last_id', None)
                post_chat = None
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat_rest_messages = None
                if last_id == '' and post_chat is not None:
                    post_chat_rest_messages = PostChatRestMessage.objects.filter(post_chat=post_chat).order_by('created')[:11]
                elif last_id != '' and post_chat is not None:
                    try:
                        last_post_chat_rest_message = PostChatRestMessage.objects.get(uuid=last_id)
                    except:
                        return JsonResponse({'res': 0})

                    post_chat_rest_messages = PostChatRestMessage.objects.filter(Q(post_chat=post_chat) & Q(pk__gt=last_post_chat_rest_message.pk)).order_by('created')[:11]
                count = 0
                next = False
                output = []
                if post_chat_rest_messages is not None:
                    for post_chat_rest_message in post_chat_rest_messages:
                        count = count + 1
                        if count == 11:
                            next = True
                            break
                        you_like = False
                        if PostChatRestMessageLike.objects.filter(user=request.user, post_chat_rest_message=post_chat_rest_message).exists():
                            you_like = True
                        sub_output = {
                            'id': post_chat_rest_message.uuid,
                            'user_id': post_chat_rest_message.user.username,
                            'name': post_chat_rest_message.user.usertextname.name,
                            'username': post_chat_rest_message.user.userusername.username,
                            'text': post_chat_rest_message.text,
                            'created': post_chat_rest_message.created,
                            'like_count': post_chat_rest_message.postchatrestmessagelikecount.count,
                            'photo': post_chat_rest_message.user.userphoto.file_50_url(),
                            'you_like': you_like,
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'rest_next': next})
        else:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                last_id = request.POST.get('last_id', None)
                post_chat = None
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat_rest_messages = None
                if last_id == '' and post_chat is not None:
                    post_chat_rest_messages = PostChatRestMessage.objects.filter(post_chat=post_chat).order_by('created')[:11]
                elif last_id != '' and post_chat is not None:
                    try:
                        last_post_chat_rest_message = PostChatRestMessage.objects.get(uuid=last_id)
                    except:
                        return JsonResponse({'res': 0})

                    post_chat_rest_messages = PostChatRestMessage.objects.filter(Q(post_chat=post_chat) & Q(pk__gt=last_post_chat_rest_message.pk)).order_by('created')[:11]
                count = 0
                next = False
                output = []
                if post_chat_rest_messages is not None:
                    for post_chat_rest_message in post_chat_rest_messages:
                        count = count + 1
                        if count == 11:
                            next = True
                            break
                        you_like = False
                        sub_output = {
                            'id': post_chat_rest_message.uuid,
                            'user_id': post_chat_rest_message.user.username,
                            'name': post_chat_rest_message.user.usertextname.name,
                            'username': post_chat_rest_message.user.userusername.username,
                            'text': post_chat_rest_message.text,
                            'created': post_chat_rest_message.created,
                            'like_count': post_chat_rest_message.postchatrestmessagelikecount.count,
                            'photo': post_chat_rest_message.user.userphoto.file_50_url(),
                            'you_like': you_like,
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'rest_next': next})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_chat_rest_like(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                rest_id = request.POST.get('rest_id', None)
                try:
                    post_chat_rest_message = PostChatRestMessage.objects.get(uuid=rest_id)
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_chat_rest_message_like = PostChatRestMessageLike.objects.get(post_chat_rest_message=post_chat_rest_message, user=request.user)
                except PostChatRestMessageLike.DoesNotExist:
                    post_chat_rest_message_like = None

                liked = None
                if post_chat_rest_message_like is not None:
                    try:
                        with transaction.atomic():
                            post_chat_rest_message_like.delete()
                            from django.db.models import F
                            post_chat_rest_message_like_count = post_chat_rest_message.postchatrestmessagelikecount
                            post_chat_rest_message_like_count.count = F('count') - 1
                            post_chat_rest_message_like_count.save()
                            liked = False
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})
                else:
                    try:
                        with transaction.atomic():
                            post_chat_rest_message_like = PostChatRestMessageLike.objects.create(post_chat_rest_message=post_chat_rest_message, user=request.user)
                            from django.db.models import F
                            post_chat_rest_message_like_count = post_chat_rest_message.postchatrestmessagelikecount
                            post_chat_rest_message_like_count.count = F('count') + 1
                            post_chat_rest_message_like_count.save()
                            liked = True
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'liked': liked})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_rest_delete(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                rest_id = request.POST.get('rest_id', None)
                try:
                    rest_message = PostChatRestMessage.objects.get(uuid=rest_id)
                except PostChatRestMessage.DoesNotExist:
                    return JsonResponse({'res': 0})
                if rest_message is not None:
                    if rest_message.user == request.user or rest_message.post_chat.post.user == request.user:

                        try:
                            with transaction.atomic():
                                rest_message.delete()
                                from django.db.models import F
                                rest_count = rest_message.post_chat.postchatrestmessagecount
                                rest_count.count = F('count') - 1
                                rest_count.save()
                                # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                        except Exception:
                            return JsonResponse({'res': 0})
                        return JsonResponse({'res': 1, 'deleted': True})

                return JsonResponse({'res': 2})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_profile_follow(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                chosen_user_id = request.POST.get('user_id', None)
                chosen_user = None
                try:
                    chosen_user = User.objects.get(username=chosen_user_id)
                except User.DoesNotExist:
                    return JsonResponse({'res': 0})

                if chosen_user is not None:
                    # 어이없는 스스로 팔로우 방지
                    if chosen_user == request.user:
                        return JsonResponse({'res': 0})
                    follow = None
                    try:
                        follow = Follow.objects.get(follow=chosen_user, user=request.user)
                    except Follow.DoesNotExist:
                        pass
                    result = None
                    if follow is not None:
                        try:
                            with transaction.atomic():
                                follow.delete()

                                from django.db.models import F
                                following_count = request.user.followingcount
                                following_count.count = F('count') - 1
                                following_count.save()
                                follower_count = chosen_user.followercount
                                follower_count.count = F('count') - 1
                                follower_count.save()
                                result = False

                                # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                        except Exception:
                            return JsonResponse({'res': 0})
                    else:
                        try:
                            with transaction.atomic():
                                follow = Follow.objects.create(follow=chosen_user, user=request.user)
                                from django.db.models import F
                                following_count = request.user.followingcount
                                following_count.count = F('count') + 1
                                following_count.save()
                                follower_count = chosen_user.followercount
                                follower_count.count = F('count') + 1
                                follower_count.save()
                                result = True

                                # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                        except Exception:
                            return JsonResponse({'res': 0})
                    return JsonResponse({'res': 1, 'result': result})

                return JsonResponse({'res': 2})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_profile_following(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                user_id = request.POST.get('user_id', None)
                next_id = request.POST.get('next_id', None)
                user = None
                try:
                    user = User.objects.get(username=user_id)
                except User.DoesNotExist:
                    pass

                next = None
                output = []
                if user is not None:
                    if next_id == '':
                        followings = Follow.objects.filter(user=user).order_by('created')[:31]
                    else:
                        try:
                            last_following = Follow.objects.get(follow__username=next_id, user=user)
                        except:
                            return JsonResponse({'res': 0})
                        followings = Follow.objects.filter(Q(user=user) & Q(pk__gte=last_following.pk)).order_by('created')[:31]
                    count = 0
                    for follow in followings:
                        count = count+1
                        if count == 31:
                            next = follow.follow.username
                            break
                        sub_output = {
                            'username': follow.follow.userusername.username,
                            'photo': follow.follow.userphoto.file_50_url(),
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next':next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_profile_follower(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                user_id = request.POST.get('user_id', None)
                next_id = request.POST.get('next_id', None)
                user = None
                try:
                    user = User.objects.get(username=user_id)
                except User.DoesNotExist:
                    pass

                next = None
                output = []
                if user is not None:
                    if next_id == '':
                        followers = Follow.objects.filter(follow=user).order_by('created')[:31]
                    else:
                        try:

                            last_follower = Follow.objects.get(follow=user, user__username=next_id)
                        except:
                            return JsonResponse({'res': 0})
                        followers = Follow.objects.filter(Q(follow=user) & Q(pk__gte=last_follower.pk)).order_by('created')[:31]
                    count = 0
                    for follow in followers:
                        count = count+1
                        if count == 31:
                            next = follow.user.username
                            break
                        sub_output = {
                            'username': follow.user.userusername.username,
                            'photo': follow.user.userphoto.file_50_url(),
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next':next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_profile_post(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                chosen_user_id = request.POST.get('chosen_user_id', None)
                last_id = request.POST.get('last_post_id', None)
                user = None
                try:
                    user = User.objects.get(username=chosen_user_id)
                except User.DoesNotExist:
                    pass
                master = False
                if user == request.user:
                    master = True
                posts = None

                if master:
                    if last_id == '':
                        posts = Post.objects.filter((Q(user=user))).order_by('-post_chat_created').distinct()[:21]
                    else:
                        last_post = None
                        try:
                            last_post = Post.objects.get(uuid=last_id)
                        except Exception as e:
                            print(e)
                            pass
                        if last_post is not None:
                            posts = Post.objects.filter((Q(user=user)) & Q(post_chat_created__lte=last_post.post_chat_created)).exclude(pk=last_post.pk).order_by('-post_chat_created').distinct()[:21]
                        else:
                            posts = Post.objects.filter(Q(user=user)).order_by('-post_chat_created').distinct()[:21]
                else:
                    if last_id == '':
                        posts = Post.objects.filter((Q(user=user) & Q(is_open=True))).order_by('-post_chat_created').distinct()[:21]
                    else:
                        last_post = None
                        try:
                            last_post = Post.objects.get(uuid=last_id)
                        except Exception as e:
                            print(e)
                            pass
                        if last_post is not None:
                            posts = Post.objects.filter((Q(user=user)) & Q(is_open=True) & Q(post_chat_created__lte=last_post.post_chat_created)).exclude(pk=last_post.pk).order_by('-post_chat_created').distinct()[:21]
                        else:
                            posts = Post.objects.filter(Q(user=user) & Q(is_open=True)).order_by('-post_chat_created').distinct()[:21]
                # 이제 리스트 만드는 코드가 필요하다. #########

                # filter(Q(post__uuid=post_id) & Q(pk__lt=last_post_chat.pk))
                ################################
                output = []
                count = 0
                last = None
                sub_output = None
                post_follow = None
                for post in posts:
                    count = count + 1
                    if count == 20:
                        last = post.uuid
                    post_follow = True
                    if Follow.objects.filter(user=request.user, follow=post.user).exists():
                        post_follow = False
                    sub_output = {
                        'id': post.uuid,
                        'created': post.created,
                        'post_follow': post_follow
                    }

                    output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'last': last, 'master': master})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_profile_post_delete(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                post = None
                try:
                    post = Post.objects.get(uuid=post_id, user=request.user)
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})
                if post is not None:
                    post.delete()

                return JsonResponse({'res': 1})

        return JsonResponse({'res': 2})
@ensure_csrf_cookie
def re_profile_populate(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                from django.db.models import Q
                name = post.user.usertextname.name
                profile_photo = post.user.userphoto.file_50_url()

                if post.has_another_profile:
                    name = post.postprofile.name
                    profile_photo = post.postprofile.file_50_url()
                you_liked = False
                if PostLike.objects.filter(user=request.user, post=post).exists():
                    you_liked = True
                post_chat_read = PostChatRead.objects.filter(post=post, user=request.user).last()
                post_chat = None
                post_chat_last_chat = None
                if post_chat_read is None:
                    try:
                        post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                    except IndexError:
                        post_chat_last_chat = {'kind': 'start'}
                    if post_chat is not None:
                        if post_chat.kind == POSTCHAT_TEXT:
                            post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                    'text': escape(post_chat.postchattext.text)}
                        elif post_chat.kind == POSTCHAT_PHOTO:
                            post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}
                else:
                    if post_chat_read.post_chat.kind == POSTCHAT_START:
                        try:
                            post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                        except IndexError:
                            post_chat_last_chat = {'kind': 'start'}
                        if post_chat is not None:
                            if post_chat.kind == POSTCHAT_TEXT:
                                post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                                  'text': escape(post_chat.postchattext.text)}
                            elif post_chat.kind == POSTCHAT_PHOTO:
                                post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say,
                                                  'url': post_chat.postchatphoto.file.url}
                    elif post_chat_read.post_chat.kind == POSTCHAT_TEXT:
                        post_chat = post_chat_read.post_chat
                        post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say, 'text': escape(post_chat.postchattext.text)}
                    elif post_chat_read.post_chat.kind == POSTCHAT_PHOTO:
                        post_chat = post_chat_read.post_chat
                        post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}

                new = True
                post_chat_last = PostChat.objects.filter(post=post).last()
                post_chat_read_last = PostChatRead.objects.filter(post=post, user=request.user).last()
                if post_chat_read_last is not None:
                    if post_chat_read_last.post_chat == post_chat_last:
                        new = False
                    else:
                        new = True

                user_follow = False
                if Follow.objects.filter(user=request.user, follow=post.user).exists():
                    user_follow = True

                post_follow = False
                if PostFollow.objects.filter(post=post, user=request.user).exists():
                    post_follow = True

                output = {'title': post.title,
                          'desc': post.description,
                          'username': post.user.userusername.username,
                          'user_id': post.user.username,
                          'name': name,
                          'photo': profile_photo,
                          'created': post.post_chat_created,
                          'last_chat': post_chat_last_chat,
                          'absolute_url': post.get_absolute_url(),
                          'id': post.uuid,
                          'like_count': post.postlikecount.count,
                          'you_liked': you_liked,
                          'comment_count': post.postcommentcount.count,
                          'three_comments': post.get_three_comments(),
                          'new': new,
                          'user_follow': user_follow,
                          'post_follow': post_follow,
                          'post_follow_count': post.postfollowcount.count,
                          }
                return JsonResponse({'res': 1, 'set': output})
        else:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                from django.db.models import Q
                name = post.user.usertextname.name
                profile_photo = post.user.userphoto.file_50_url()

                if post.has_another_profile:
                    name = post.postprofile.name
                    profile_photo = post.postprofile.file_50_url()
                you_liked = False
                post_chat_read = None
                post_chat = None
                post_chat_last_chat = None
                if post_chat_read is None:
                    try:
                        post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                    except IndexError:
                        post_chat_last_chat = {'kind': 'start'}
                    if post_chat is not None:
                        if post_chat.kind == POSTCHAT_TEXT:
                            post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                    'text': escape(post_chat.postchattext.text)}
                        elif post_chat.kind == POSTCHAT_PHOTO:
                            post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}

                new = True

                user_follow = False

                post_follow = False

                output = {'title': post.title,
                          'desc': post.description,
                          'username': post.user.userusername.username,
                          'user_id': post.user.username,
                          'name': name,
                          'photo': profile_photo,
                          'created': post.created,
                          'last_chat': post_chat_last_chat,
                          'absolute_url': post.get_absolute_url(),
                          'id': post.uuid,
                          'like_count': post.postlikecount.count,
                          'you_liked': you_liked,
                          'comment_count': post.postcommentcount.count,
                          'three_comments': post.get_three_comments(),
                          'new': new,
                          'user_follow': user_follow,
                          'post_follow': post_follow,
                          'post_follow_count': post.postfollowcount.count,
                          }
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_like_list(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                next_id = request.POST.get('next_id', None)
                post = None
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 1})

                next = None
                output = []
                if post is not None:
                    if next_id == '':
                        likes = PostLike.objects.filter(post=post).order_by('created')[:31]
                    else:
                        try:

                            last_like = PostLike.objects.get(post=post, user__username=next_id)
                        except:
                            return JsonResponse({'res': 0})
                        likes = PostLike.objects.filter(Q(post=post) & Q(pk__gte=last_like.pk)).order_by('created')[:31]
                    count = 0
                    for like in likes:
                        count = count+1
                        if count == 31:
                            next = like.user.username
                            break
                        sub_output = {
                            'username': like.user.userusername.username,
                            'photo': like.user.userphoto.file_50_url(),
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_like_list(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                next_id = request.POST.get('next_id', None)
                post_chat = None
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 1})

                next = None
                output = []
                if post_chat is not None:
                    if next_id == '':
                        likes = PostChatLike.objects.filter(post_chat=post_chat).order_by('created')[:31]
                    else:
                        try:

                            last_like = PostChatLike.objects.get(post_chat=post_chat, user__username=next_id)
                        except:
                            return JsonResponse({'res': 0})
                        likes = PostChatLike.objects.filter(Q(post_chat=post_chat) & Q(pk__gte=last_like.pk)).order_by('created')[:31]
                    count = 0
                    for like in likes:
                        count = count+1
                        if count == 31:
                            next = like.user.username
                            break
                        sub_output = {
                            'username': like.user.userusername.username,
                            'photo': like.user.userphoto.file_50_url(),
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_rest_like_list(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_rest_id = request.POST.get('post_chat_rest_id', None)
                next_id = request.POST.get('next_id', None)
                post_chat_rest_message = None
                try:
                    post_chat_rest_message = PostChatRestMessage.objects.get(uuid=post_chat_rest_id)
                except:
                    return JsonResponse({'res': 0})

                next = None
                output = []
                if post_chat_rest_message is not None:
                    if next_id == '':
                        likes = PostChatRestMessageLike.objects.filter(post_chat_rest_message=post_chat_rest_message).order_by('created')[:31]
                    else:
                        try:

                            last_like = PostChatRestMessageLike.objects.get(post_chat_rest_message=post_chat_rest_message, user__username=next_id)
                        except:
                            return JsonResponse({'res': 0})
                        likes = PostChatRestMessageLike.objects.filter(Q(post_chat_rest_message=post_chat_rest_message) & Q(pk__gte=last_like.pk)).order_by('created')[:31]
                    count = 0
                    for like in likes:
                        count = count+1
                        if count == 31:
                            next = like.user.username
                            break
                        sub_output = {
                            'username': like.user.userusername.username,
                            'photo': like.user.userphoto.file_50_url(),
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_follow(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                post = None
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                post_follow = None
                try:
                    post_follow = PostFollow.objects.get(post=post, user=request.user)
                except PostFollow.DoesNotExist:
                    post_follow = None

                follow = None
                if post_follow is not None:
                    try:
                        with transaction.atomic():
                            post_follow.delete()
                            from django.db.models import F
                            post_follow_count = post.postfollowcount
                            post_follow_count.count = F('count') - 1
                            post_follow_count.save()
                            follow = False
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})
                else:
                    try:
                        with transaction.atomic():
                            post_follow = PostFollow.objects.create(post=post, user=request.user)
                            from django.db.models import F
                            post_follow_count = post.postfollowcount
                            post_follow_count.count = F('count') + 1
                            post_follow_count.save()
                            follow = True
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'follow': follow})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_follow_list(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                next_id = request.POST.get('next_id', None)
                post = None
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})

                next = None
                output = []
                post_follows = None
                if post is not None:
                    if next_id == '':
                        post_follows = PostFollow.objects.filter(post=post).order_by('created')[:31]
                    else:
                        try:

                            last_post_follow = PostFollow.objects.get(post=post, user__username=next_id)
                        except:
                            return JsonResponse({'res': 0})
                        post_follows = PostFollow.objects.filter(Q(post=post) & Q(pk__gte=last_post_follow.pk)).order_by('created')[:31]
                    count = 0
                    for post_follow in post_follows:
                        count = count+1
                        if count == 31:
                            next = post_follow.user.username
                            break
                        sub_output = {
                            'username': post_follow.user.userusername.username,
                            'photo': post_follow.user.userphoto.file_50_url(),
                        }
                        output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_explore_feed(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                last_id = request.POST.get('last_id', None)
                posts = None
                if last_id == '':
                    posts = Post.objects.filter(~Q(user__is_followed__user=request.user) & Q(is_open=True) & ~Q(user=request.user)).exclude(
                        Q(post_follow__user=request.user)).order_by('-post_chat_created').distinct()[:20]
                else:
                    last_post = None
                    try:
                        last_post = Post.objects.get(uuid=last_id)
                    except Exception as e:
                        print(e)
                        return JsonResponse({'res': 0})
                    posts = Post.objects.filter(~Q(user__is_followed__user=request.user) & Q(is_open=True) & Q(post_chat_created__lte=last_post.post_chat_created) & ~Q(user=request.user)).exclude(
                        Q(post_follow__user=request.user) | Q(uuid=last_id)).order_by('-post_chat_created').distinct()[:20]

                # 여기서 posts 옵션 준다. 20개씩 줄 것이므로 21로 잡는다. #########
                # 여기서 포스트 팔로우 된 건 피드에 뜨지 않게 Q 설정해야한다 .
                ################################
                output = []
                count = 0
                last = None
                post_follow = None
                for post in posts:
                    count = count + 1
                    if count == 20:
                        last = post.uuid
                    sub_output = {
                        'id': post.uuid,
                    }

                    output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'last': last})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_note_all(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                next_id = request.POST.get('next_id', None)
                notices = None
                if next_id == '':
                    notices = Notice.objects.filter(Q(user=request.user)).order_by('-created').distinct()[:31]
                else:
                    next_notice = None
                    try:
                        next_notice = Notice.objects.get(uuid=next_id)
                    except Exception as e:
                        print(e)
                        return JsonResponse({'res': 0})
                    notices = Notice.objects.filter(Q(user=request.user) & Q(pk__lte=next_notice.pk)).order_by('-created').distinct()[:31]

                # 여기서 posts 옵션 준다. 20개씩 줄 것이므로 21로 잡는다. #########
                # 여기서 포스트 팔로우 된 건 피드에 뜨지 않게 Q 설정해야한다 .
                ################################
                output = []
                count = 0
                next = None
                for notice in notices:
                    count = count + 1
                    if count == 31:
                        next = notice.uuid
                        break
                    sub_output = {
                        'id': notice.uuid,
                        'created': notice.created,
                        'notice_kind': notice.kind,
                        'notice_value': notice.get_value(),
                    }

                    output.append(sub_output)

                return JsonResponse({'res': 1, 'set': output, 'next': next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_nav_badge_populate(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                try:
                    notice_count = request.user.noticecount.count
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'notice_count': notice_count})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_search_all(request):
    if request.method == "POST":
        if request.is_ajax():
            search_word = request.POST.get('search_word', None)
            users = User.objects.filter(Q(userusername__username__icontains=search_word)
                                        | Q(usertextname__name__icontains=search_word)).order_by('-noticecount__created').distinct()[:11]
            user_output = []
            users_count = 0
            user_next = None
            for user in users:
                users_count = users_count + 1
                if users_count == 11:
                    user_next = True
                    break
                sub_output = {
                    'username': user.userusername.username,
                    'user_photo': user.userphoto.file_50_url(),
                    'user_text_name': user.usertextname.name,
                }

                user_output.append(sub_output)

            posts = Post.objects.filter(Q(user__userusername__username__icontains=search_word)
                                        | Q(title__icontains=search_word)
                                        | Q(description__icontains=search_word)
                                        | Q(user__usertextname__name__icontains=search_word)).order_by('-post_chat_created').distinct()[:11]

            post_output = []
            posts_count = 0
            post_next = None
            for post in posts:
                posts_count = posts_count + 1
                if posts_count == 11:
                    post_next = True
                    break

                if request.user.is_authenticated:
                    post_follow = True
                    if Follow.objects.filter(user=request.user, follow=post.user).exists():
                        post_follow = False
                else:
                    post_follow = False
                sub_output = {
                    'id': post.uuid,
                    'created': post.created,
                    'post_follow': post_follow
                }

                post_output.append(sub_output)
            return JsonResponse({'res': 1,
                                 'user_set': user_output,
                                 'user_next': user_next,
                                 'post_set': post_output,
                                 'post_next': post_next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_search_user(request):
    if request.method == "POST":
        if request.is_ajax():
            search_word = request.POST.get('search_word', None)
            next_id = request.POST.get('next_id', None)
            if next_id == '':
                users = User.objects.filter(Q(userusername__username__icontains=search_word)
                                            | Q(usertextname__name__icontains=search_word)).order_by('-noticecount__created').distinct()[:31]
            else:
                next_user = None
                try:
                    next_user = User.objects.get(username=next_id)
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})

                users = User.objects.filter((Q(userusername__username__icontains=search_word)
                                            | Q(usertextname__name__icontains=search_word)) & Q(noticecount__created__lte=next_user.noticecount.created)).exclude(pk=next_user.pk).order_by(
                    '-noticecount__created').distinct()[:31]
            user_output = []
            users_count = 0
            user_next = None
            for user in users:
                users_count = users_count + 1
                if users_count == 31:
                    user_next = user.username
                    break
                sub_output = {
                    'username': user.userusername.username,
                    'user_photo': user.userphoto.file_50_url(),
                    'user_text_name': user.usertextname.name,
                }

                user_output.append(sub_output)

            return JsonResponse({'res': 1,
                                 'user_set': user_output,
                                 'user_next': user_next})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_search_post(request):
    if request.method == "POST":
        if request.is_ajax():
            search_word = request.POST.get('search_word', None)
            next_id = request.POST.get('next_id', None)
            if next_id == '':
                posts = Post.objects.filter(Q(user__userusername__username__icontains=search_word)
                                            | Q(title__icontains=search_word)
                                            | Q(description__icontains=search_word)
                                            | Q(user__usertextname__name__icontains=search_word)).order_by(
                    '-post_chat_created').distinct()[:2]
            else:
                next_post = None
                try:
                    next_post = Post.objects.get(uuid=next_id)
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})

                posts = Post.objects.filter((Q(user__userusername__username__icontains=search_word)
                                            | Q(title__icontains=search_word)
                                            | Q(description__icontains=search_word)
                                            | Q(user__usertextname__name__icontains=search_word))
                                            & Q(post_chat_created__lte=next_post.post_chat_created)).order_by('-post_chat_created').distinct()[:2]

            post_output = []
            posts_count = 0
            post_next = None
            for post in posts:
                posts_count = posts_count + 1
                if posts_count == 2:
                    post_next = post.uuid
                    break

                sub_output = {
                    'id': post.uuid,
                }

                post_output.append(sub_output)
            return JsonResponse({'res': 1,
                                 'post_set': post_output,
                                 'post_next': post_next})

        return JsonResponse({'res': 2})

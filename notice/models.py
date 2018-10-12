from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from authapp.models import *
from object.models import *
from relation.models import *
import uuid
from django.utils.html import escape, _js_escapes, normalize_newlines

# For Post Things
# 페이지픽에서 공개 비공개와 별개로 등록 비등록이 중요하다. 어차피 등록될 때 누가 등록했는지는 안 뜨게 했었다.
# booleanfield로 대충 하고 꼭 어쩔 수 없는 것만 textfield 로 한다. 보통 3가지 경우 나오는 것.
# private , public은 나중에 한다. 귀찮다.

FOLLOW = 1001
POST_FOLLOW = 2001
POST_COMMENT = 2002
POST_LIKE = 2003
POST_CHAT_LIKE = 3001
POST_CHAT_REST = 4001
POST_CHAT_REST_LIKE = 4002

KINDS_CHOICES = (
    (FOLLOW, "follow"),
    (POST_FOLLOW, "post_follow"),
    (POST_COMMENT, "post_comment"),
    (POST_LIKE, "post_like"),
    (POST_CHAT_LIKE, "post_chat_like"),
    (POST_CHAT_REST, "post_chat_rest"),
    (POST_CHAT_REST_LIKE, "post_chat_rest_like"),
)


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    kind = models.PositiveSmallIntegerField(choices=KINDS_CHOICES, default=0)
    checked = models.BooleanField(default=False)
    uuid = models.CharField(max_length=34, unique=True, null=True, default=None)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice pk: %s, user: %s, kind: %s" % (self.pk, self.user.userusername.username, self.kind)

    def get_value(self):
        result = None
        get_result = None
        if self.kind == FOLLOW:
            try:
                get_result = self.noticefollow.follow
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {'username': get_result.user.userusername.username,
                          'user_photo': get_result.user.userphoto.file_50_url()}
            return result
        elif self.kind == POST_FOLLOW:
            try:
                get_result = self.noticepostfollow.post_follow
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {'post_id': get_result.post.uuid,
                          'username': get_result.user.userusername.username,
                          'user_photo': get_result.user.userphoto.file_50_url()}
            return result
        elif self.kind == POST_COMMENT:
            try:
                get_result = self.noticepostcomment.post_comment
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {'post_id': get_result.post.uuid,
                          'username': get_result.user.userusername.username,
                          'user_photo': get_result.user.userphoto.file_50_url(),
                          'comment_text': escape(get_result.text)[0:10]}
            return result
        elif self.kind == POST_LIKE:
            try:
                get_result = self.noticepostlike.post_like
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {
                    'post_id': get_result.post.uuid,
                    'username': get_result.user.userusername.username,
                    'user_photo': get_result.user.userphoto.file_50_url()
                }
            return result
        elif self.kind == POST_CHAT_LIKE:
            try:
                get_result = self.noticepostchatlike.post_chat_like
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {
                    'post_chat_id': get_result.post_chat.uuid,
                    'username': get_result.user.userusername.username,
                    'user_photo': get_result.user.userphoto.file_50_url(),
                    'post_id': get_result.post_chat.post.uuid,
                }
            return result
        elif self.kind == POST_CHAT_REST:
            try:
                get_result = self.noticepostchatrest.post_chat_rest
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {
                    'post_chat_rest_id': get_result.uuid,
                    'post_chat_id': get_result.post_chat.uuid,
                    'post_id': get_result.post_chat.post.uuid,
                    'username': get_result.user.userusername.username,
                    'user_photo': get_result.user.userphoto.file_50_url(),
                    'post_chat_rest_text': escape(get_result.text)[0:10],
                }
            return result
        elif self.kind == POST_CHAT_REST_LIKE:
            try:
                get_result = self.noticepostchatrestlike.post_chat_rest_like
            except Exception as e:
                print(e)
                pass
            if get_result is not None:
                result = {
                    'post_chat_rest_id': get_result.post_chat_rest_message.uuid,
                    'post_chat_id': get_result.post_chat_rest_message.post_chat.uuid,
                    'post_id': get_result.post_chat_rest_message.post_chat.post.uuid,
                    'username': get_result.user.userusername.username,
                    'user_photo': get_result.user.userphoto.file_50_url(),
                    'post_chat_rest_text': escape(get_result.post_chat_rest_message.text)[0:10],
                }
            return result
        return None


class NoticeCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user: %s, count: %s" % (self.user, self.count)


class NoticeFollow(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, follow_user: %s" % (self.notice.pk, self.follow.user.userusername.username)


class NoticePostFollow(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    post_follow = models.ForeignKey(PostFollow, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, post_follow_user: %s" % (self.notice.pk, self.post_follow.user.userusername.username)


class NoticePostComment(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, post_comment_user: %s" % (self.pk, self.post_comment.user.userusername.username)


class NoticePostLike(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    post_like = models.ForeignKey(PostLike, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, post_like_user: %s" % (self.pk, self.post_like.user.userusername.username)


class NoticePostChatLike(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    post_chat_like = models.ForeignKey(PostChatLike, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, post_chat_like_user: %s" % (self.pk, self.post_chat_like.user.userusername.username)


class NoticePostChatRest(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    post_chat_rest = models.ForeignKey(PostChatRestMessage, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, post_chat_rest_user: %s" % (self.pk, self.post_chat_rest.user.userusername.username)


class NoticePostChatRestLike(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, null=True, blank=True)
    post_chat_rest_like = models.ForeignKey(PostChatRestMessageLike, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notice_pk: %s, post_chat_rest_like_user: %s" % (self.pk, self.post_chat_rest_like.user.userusername.username)
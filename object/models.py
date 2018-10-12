from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from authapp.models import *
from .disposers import *
import uuid
from django.utils.html import escape, _js_escapes, normalize_newlines
from django.utils.timezone import now
# For Post Things
# 페이지픽에서 공개 비공개와 별개로 등록 비등록이 중요하다. 어차피 등록될 때 누가 등록했는지는 안 뜨게 했었다.
# booleanfield로 대충 하고 꼭 어쩔 수 없는 것만 textfield 로 한다. 보통 3가지 경우 나오는 것.
# private , public은 나중에 한다. 귀찮다.


class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(max_length=1000, null=True, blank=True, default=None)
    description = models.TextField(max_length=2000, null=True, blank=True, default=None)
    has_another_profile = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    uuid = models.CharField(max_length=34, unique=True, null=True, default=None)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    post_chat_created = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return "Post pk: %s, user: %s" % (self.pk, self.user.userusername.username)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('baseapp:post', kwargs={'uuid': self.uuid})

    def get_last_chat(self):
        try:
            post_chat = PostChat.objects.filter(post__uuid=self.uuid).order_by('created')[1]
        except IndexError:
            return {'kind': 'start'}
        print(str(post_chat.kind))
        if post_chat.kind == POSTCHAT_TEXT:
            return {'kind': 'text', 'you_say': post_chat.you_say, 'text': escape(post_chat.postchattext.text)}
        elif post_chat.kind == POSTCHAT_PHOTO:
            return {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}

    def get_three_comments(self):

        post_comments = PostComment.objects.filter(post__uuid=self.uuid).order_by('created')[:3]
        post_comment_uuids = [post_comment.uuid for post_comment in post_comments]
        output = []
        post_comment = None
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
        else:
            output = None
        return output


class PostFirstCheck(models.Model):
    post = models.OneToOneField("Post", on_delete=models.CASCADE, null=True, blank=True)
    first_checked = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Post pk: %s" % self.post.pk


class PostProfile(models.Model):
    post = models.OneToOneField("Post", on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=30, null=True, blank=True)

    file_50 = models.ImageField(null=True, blank=True, default=None, upload_to=get_file_path_post_profile_50)
    file_300 = models.ImageField(null=True, blank=True, default=None, upload_to=get_file_path_post_profile_300)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "PostPhoto pk: %s, username: %s" % (self.pk, self.post.user.userusername.username)

    def file_50_url(self):
        if self.file_50:
            return self.file_50.url
        return "/media/default/default_photo_50.png"

    def file_300_url(self):
        if self.file_300:
            return self.file_300.url
        return "/media/default/default_photo_300.png"

from .numbers import *
KINDS_CHOICES = (
    (POSTCHAT_START, "start"),
    (POSTCHAT_TEXT, "text"),
    (POSTCHAT_PHOTO, "photo"),
)


class PostChat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    you_say = models.BooleanField(default=True)
    before = models.ForeignKey("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    kind = models.PositiveSmallIntegerField(choices=KINDS_CHOICES, default=0)
    uuid = models.CharField(max_length=34, unique=True, default=uuid.uuid4().hex)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.before is None:
            before_pk = None
        else:
            before_pk = self.before.pk
        return "postchat pk: %s, before: %s, kind: %s" % (self.pk, before_pk, self.kind)

    def get_value(self):
        if self.kind == POSTCHAT_TEXT:
            post_chat_data = None
            try:
                post_chat_data = self.postchattext
            except:
                return 'error'
            # 여기서 스크립트 없애는 태그 걸어줘야 한다.
            return {'kind': 'text', 'you_say': self.you_say, 'text': escape(post_chat_data.text), 'id': self.uuid}
        elif self.kind == POSTCHAT_PHOTO:
            post_chat_data = None
            try:
                post_chat_data = self.postchatphoto
            except:
                return 'error'
            return {'kind': 'photo', 'you_say': self.you_say, 'url': post_chat_data.file.url, 'id': self.uuid}
        elif self.kind == POSTCHAT_START:
            return {'kind': 'start'}

    def get_raw_value(self):
        if self.kind == POSTCHAT_TEXT:
            post_chat_data = None
            try:
                post_chat_data = self.postchattext
            except:
                return 'error'
            return escape(post_chat_data.text)
        elif self.kind == POSTCHAT_PHOTO:
            post_chat_data = None
            try:
                post_chat_data = self.postchatphoto
            except:
                return 'error'
            return post_chat_data.file.url
        elif self.kind == POSTCHAT_START:
            return 'start'

class PostChatRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    post_chat = models.ForeignKey("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user: %s, postchat: %s" % (self.user.userusername.username, self.post_chat.uuid)

    class Meta:
        unique_together = ('user', 'post_chat',)


class PostChatText(models.Model):
    post_chat = models.OneToOneField("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "postchat text: %s" % self.pk


class PostChatPhoto(models.Model):
    post_chat = models.OneToOneField("PostChat", on_delete=models.CASCADE, null=True, blank=True)

    file = models.ImageField(null=True, blank=True, default=None, upload_to=get_file_path_post_chat_photo)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post chat photo: %s" % self.pk


class PostChatRestMessage(models.Model):
    post_chat = models.ForeignKey("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    uuid = models.CharField(max_length=34, unique=True, default=uuid.uuid4().hex)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post chat rest message: %s, post_chat: %s" % (self.pk, self.post_chat.pk)


class PostChatRestMessageCount(models.Model):
    post_chat = models.OneToOneField("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post chat: %s" % self.pk


class PostComment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    uuid = models.CharField(max_length=34, unique=True, default=uuid.uuid4().hex)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post comment: %s" % self.pk


class PostCommentCount(models.Model):
    post = models.OneToOneField("Post", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post comment: %s" % self.pk

# 내용 없는 OneToOneField 는 의미없다. kind 같은 내용이라도 있어야 OneToOneField 가 존재할 이유가 있음.
# 내용 없는 OneToOneField 는 거의 필요없다. 과욕이다.


class PostLike(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post Like: %s" % self.pk

    class Meta:
        unique_together = ('user', 'post',)


class PostLikeCount(models.Model):
    post = models.OneToOneField("Post", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post Like Count: %s" % self.pk


class PostChatLike(models.Model):
    post_chat = models.ForeignKey("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post Chat Like: %s" % self.pk

    class Meta:
        unique_together = ('user', 'post_chat',)


class PostChatLikeCount(models.Model):
    post_chat = models.OneToOneField("PostChat", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post Chat Like Count: %s" % self.pk


class PostChatRestMessageLike(models.Model):
    post_chat_rest_message = models.ForeignKey("PostChatRestMessage", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post Chat Rest Message Like: %s" % self.pk

    class Meta:
        unique_together = ('user', 'post_chat_rest_message',)


class PostChatRestMessageLikeCount(models.Model):
    post_chat_rest_message = models.OneToOneField("PostChatRestMessage", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post chat rest message Like Count: %s" % self.pk


class PostFollow(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post_follow')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='post_follow')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post_follow user: %s, post_pk: %s" % (self.user.userusername.username, self.post.pk)

    class Meta:
        unique_together = ('post', 'user',)


class PostFollowCount(models.Model):
    post = models.OneToOneField("Post", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "post Like Count: %s" % self.pk



# PostChat 이랑 PostComment 에 좋아요 구현, PostRest 는 보류. 안 하는 게 나을 것 같다. 아냐 하는 게 나을 것 같아.
# 글을 많이 쓰게 하는 것이 원칙인데 구현하면 제안을 많이 쓰게 할 수 있다. 그러나 구현하지 않는다면 제안이 줄기 때문에 독창적인 사람만
# 글을 쓰는 데에 스트레스를 덜 주게 된다. 그러나 독창적인 사람의 경우 남의 의견이 어떻든 상관하지 않을 수 있기 때문에 효과는 미미할
# 것으로 예상한다. 필요하다면 제안을 제한하거나 제안을 장막으로 가리는 등의 도움이 될 수 있다. 글을 많이 쓰고 활동하게 하는 것이
# 우선이다. 원칙과 우선순위. 우선순위와 원칙. 우선순위와 예외와 규칙.
# ----------------------------------------------------------------------------------------------------------------------

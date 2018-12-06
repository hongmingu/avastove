from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from object.models import *
from relation.models import *
from notice.models import *
from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from object.numbers import *

KINDS_CHOICES = (
    (POSTCHAT_START, "start"),
    (POSTCHAT_TEXT, "text"),
    (POSTCHAT_PHOTO, "photo"),
)


@receiver(post_save, sender=PostChat)
def created_post_chat(sender, instance, created, **kwargs):
    if created:
        if instance.kind != POSTCHAT_START:
            PostChatLikeCount.objects.create(post_chat=instance)
        PostChatRestMessageCount.objects.create(post_chat=instance)
        post = instance.post
        post.post_chat_created = now()
        post.save()


@receiver(post_save, sender=PostChatRestMessage)
def created_post_rest_message(sender, instance, created, **kwargs):
    if created:
        PostChatRestMessageLikeCount.objects.create(post_chat_rest_message=instance)


# notice follow

@receiver(post_save, sender=Follow)
def created_follow(sender, instance, created, **kwargs):
    if created:

        try:
            with transaction.atomic():
                if not instance.user == instance.follow:
                    notice = Notice.objects.create(user=instance.follow, kind=FOLLOW, uuid=uuid.uuid4().hex)
                    notice_follow = NoticeFollow.objects.create(notice=notice, follow=instance)

                following_count = instance.user.followingcount
                following_count.count = F('count') + 1
                following_count.save()
                follower_count = instance.follow.followercount
                follower_count.count = F('count') + 1
                follower_count.save()
        except Exception as e:
            print(e)
            pass


@receiver(post_delete, sender=Follow)#이걸 pre_delete로 해야하나?
def deleted_follow(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            following_count = instance.user.followingcount
            following_count.count = F('count') - 1
            following_count.save()
            follower_count = instance.follow.followercount
            follower_count.count = F('count') - 1
            follower_count.save()
    except Exception as e:
        print(e)
        pass


@receiver(post_delete, sender=NoticeFollow)#이걸 pre_delete로 해야하나?
def deleted_notice_follow(sender, instance, **kwargs):
    if instance.notice:
        try:
            with transaction.atomic():
                instance.notice.delete()
        except Exception as e:
            print(e)
            pass


# notice post_follow


@receiver(post_save, sender=PostFollow)
def created_post_follow(sender, instance, created, **kwargs):
    if created:

        try:
            with transaction.atomic():
                if not instance.user == instance.post.user:
                    notice = Notice.objects.create(user=instance.post.user, kind=POST_FOLLOW, uuid=uuid.uuid4().hex)
                    notice_post_follow = NoticePostFollow.objects.create(notice=notice, post_follow=instance)

                post_follow_count = instance.post.postfollowcount
                post_follow_count.count = F('count') + 1
                post_follow_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=PostFollow)#이걸 pre_delete로 해야하나?
def deleted_post_follow(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            post_follow_count = instance.post.postfollowcount
            post_follow_count.count = F('count') - 1
            post_follow_count.save()
    except Exception:
        pass

@receiver(post_delete, sender=NoticePostFollow)#이걸 pre_delete로 해야하나?
def deleted_notice_post_follow(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.notice.delete()
    except Exception:
        pass


# notice post_comment
@receiver(post_save, sender=PostComment)
def created_post_comment(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():

                if not instance.user == instance.post.user:
                    notice = Notice.objects.create(user=instance.post.user, kind=POST_COMMENT, uuid=uuid.uuid4().hex)
                    notice_post_comment = NoticePostComment.objects.create(notice=notice, post_comment=instance)

                post_comment_count = instance.post.postcommentcount
                post_comment_count.count = F('count') + 1
                post_comment_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=PostComment)  # 이걸 pre_delete로 해야하나?
def deleted_post_comment(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            post_comment_count = instance.post.postcommentcount
            post_comment_count.count = F('count') - 1
            post_comment_count.save()

    except Exception:
        pass


@receiver(post_delete, sender=NoticePostComment)#이걸 pre_delete로 해야하나?
def deleted_notice_post_comment(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.notice.delete()
    except Exception:
        pass


# notice post_like
@receiver(post_save, sender=PostLike)
def created_post_like(sender, instance, created, **kwargs):
    if created:

        try:
            with transaction.atomic():
                if not instance.user == instance.post.user:
                    notice = Notice.objects.create(user=instance.post.user, kind=POST_LIKE, uuid=uuid.uuid4().hex)
                    notice_post_like = NoticePostLike.objects.create(notice=notice, post_like=instance)

                post_like_count = instance.post.postlikecount
                post_like_count.count = F('count') + 1
                post_like_count.save()
        except Exception as e:
            print(e)
            pass


@receiver(post_delete, sender=PostLike)#이걸 pre_delete로 해야하나?
def deleted_post_like(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            from django.db.models import F
            post_like_count = instance.post.postlikecount
            post_like_count.count = F('count') - 1
            post_like_count.save()
    except Exception as e:
        print(e)
        pass


@receiver(post_delete, sender=NoticePostLike)#이걸 pre_delete로 해야하나?
def deleted_notice_post_like(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.notice.delete()
    except Exception as e:
        print(e)
        pass



# notice post_chat_like
@receiver(post_save, sender=PostChatLike)
def created_post_chat_like(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                if not instance.user == instance.post_chat.post.user:
                    notice = Notice.objects.create(user=instance.post_chat.post.user, kind=POST_CHAT_LIKE, uuid=uuid.uuid4().hex)
                    notice_post_chat_like = NoticePostChatLike.objects.create(notice=notice, post_chat_like=instance)

                post_chat_like_count = instance.post_chat.postchatlikecount
                post_chat_like_count.count = F('count') + 1
                post_chat_like_count.save()
        except Exception as e:
            print(e)
            pass


@receiver(post_delete, sender=PostChatLike)#이걸 pre_delete로 해야하나?
def deleted_post_chat_like(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            from django.db.models import F
            post_chat_like_count = instance.post_chat.postchatlikecount
            post_chat_like_count.count = F('count') - 1
            post_chat_like_count.save()
    except Exception as e:
        print(e)
        pass

@receiver(post_delete, sender=NoticePostChatLike)#이걸 pre_delete로 해야하나?
def deleted_notice_post_chat_like(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.notice.delete()
    except Exception as e:
        print(e)
        pass


# notice post_chat_rest
@receiver(post_save, sender=PostChatRestMessage)
def created_post_chat_rest(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                if not instance.user == instance.post_chat.post.user:
                    notice = Notice.objects.create(user=instance.post_chat.post.user, kind=POST_CHAT_REST, uuid=uuid.uuid4().hex)
                    notice_post_chat_rest = NoticePostChatRest.objects.create(notice=notice, post_chat_rest=instance)

                post_chat_rest_message_count = instance.post_chat.postchatrestmessagecount
                post_chat_rest_message_count.count = F('count') + 1
                post_chat_rest_message_count.save()
        except Exception as e:
            print(e)
            pass

@receiver(post_delete, sender=PostChatRestMessage)#이걸 pre_delete로 해야하나?
def deleted_post_chat_rest(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            from django.db.models import F
            rest_count = instance.post_chat.postchatrestmessagecount
            rest_count.count = F('count') - 1
            rest_count.save()
    except Exception as e:
        print(e)
        pass


@receiver(post_delete, sender=NoticePostChatRest)#이걸 pre_delete로 해야하나?
def deleted_notice_post_chat_rest(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.notice.delete()
    except Exception as e:
        print(e)
        pass

# notice post_chat_rest_like
@receiver(post_save, sender=PostChatRestMessageLike)
def created_post_chat_rest_like(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                if not instance.user == instance.post_chat_rest_message.user:
                    notice = Notice.objects.create(user=instance.user, kind=POST_CHAT_REST_LIKE, uuid=uuid.uuid4().hex)
                    notice_post_chat_rest_like = NoticePostChatRestLike.objects.create(notice=notice, post_chat_rest_like=instance)

                post_chat_rest_message_like_count = instance.post_chat_rest_message.postchatrestmessagelikecount
                post_chat_rest_message_like_count.count = F('count') + 1
                post_chat_rest_message_like_count.save()
        except Exception as e:
            print(e)
            pass

@receiver(post_delete, sender=PostChatRestMessageLike)#이걸 pre_delete로 해야하나?
def deleted_post_chat_rest_like(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            post_chat_rest_message_like_count = instance.post_chat_rest_message.postchatrestmessagelikecount
            post_chat_rest_message_like_count.count = F('count') - 1
            post_chat_rest_message_like_count.save()
    except Exception as e:
        print(e)
        pass


@receiver(post_delete, sender=NoticePostChatRestLike)#이걸 pre_delete로 해야하나?
def deleted_notice_post_chat_rest_like(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.notice.delete()
    except Exception as e:
        print(e)
        pass


@receiver(post_save, sender=Notice)
def created_notice(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice_count = instance.user.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception as e:
            print(e)
            pass


@receiver(post_delete, sender=Notice)
def deleted_notice(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            if instance.checked is False:
                notice_count = instance.user.noticecount
                notice_count.count = F('count') - 1
                notice_count.save()
    except Exception as e:
        print(e)
        pass
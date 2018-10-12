
import uuid
import os


def get_file_path_post_profile_300(instance, filename):
    ext = filename.split('.')[-1]
    usernum =instance.post.user.username

    from django.utils.timezone import now
    now = now()
    now_date = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = "300_%s_%s.%s" % (now_date, uuid.uuid4(), ext)

    return os.path.join('photo/%s/post_profile/%s' % (usernum, instance.post.pk), filename)


def get_file_path_post_profile_50(instance, filename):
    ext = filename.split('.')[-1]
    usernum = instance.post.user.username

    from django.utils.timezone import now
    now = now()
    now_date = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = "50_%s_%s.%s" % (now_date, uuid.uuid4(), ext)

    return os.path.join('photo/%s/post_profile/%s' % (usernum, instance.post.pk), filename)


def get_file_path_post_chat_photo(instance, filename):
    ext = filename.split('.')[-1]
    usernum = instance.post_chat.post.user.username

    from django.utils.timezone import now
    now = now()
    now_date = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = "_%s_%s.%s" % (now_date, uuid.uuid4(), ext)

    return os.path.join('photo/%s/post_chat_photo/%s' % (usernum, instance.post_chat.post.pk), filename)


def get_file_path_post_chat_photo_50(instance, filename):
    ext = filename.split('.')[-1]
    usernum = instance.user.username

    from django.utils.timezone import now
    now = now()
    now_date = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = "50_%s_%s.%s" % (now_date, uuid.uuid4(), ext)

    return os.path.join('photo/%s/post_chat_photo' % usernum, filename)
import json
import urllib
from urllib.parse import urlparse

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
from relation.models import FollowerCount, FollowingCount
from notice.models import NoticeCount
from .forms import *
from .models import *
from .token import *
from .utils import *

from django.contrib.auth import update_session_auth_hash



def main_create_log_in(request):
    if request.method == 'POST':
        if request.POST['type'] == 'create_first':

            form = UserCreateForm(request.POST)

            name = form.data['name']
            username = form.data['username']
            email = form.data['email']
            data = {
                'name': name,
                'username': username,
                'email': email,
            }
            username = username.lower()

            # Integrity UserEmail and UserUsername



            user_username_exist = UserUsername.objects.filter(username=username).exists()
            if user_username_exist:
                return render_with_clue_loginform_createform(request, 'authapp/main_first.html',
                                                             texts.USERNAME_ALREADY_USED, LoginForm(), UserCreateForm(data))

            username_failure = user_username_failure_validate(username)
            if username_failure:
                clue_message = None
                if username_failure is 1:
                    clue_message = texts.USERNAME_UNAVAILABLE
                elif username_failure is 2:
                    clue_message = texts.USERNAME_LENGTH_PROBLEM
                elif username_failure is 3:
                    clue_message = texts.USERNAME_8_CANNOT_DIGITS
                elif username_failure is 4:
                    clue_message = texts.USERNAME_BANNED

                return render_with_clue_loginform_createform(request, 'authapp/main_first.html',
                                                             clue_message, LoginForm(), UserCreateForm(data))

            primary_email_exist = UserPrimaryEmail.objects.filter(email=email).exists()
            if primary_email_exist:
                return render_with_clue_loginform_createform(request, 'authapp/main_first.html',
                                                             texts.EMAIL_ALREADY_USED, LoginForm(), UserCreateForm(data))
            email_failure = user_primary_email_failure_validate(email)
            if email_failure:
                clue_message = None
                if email_failure is 1:
                    clue_message = texts.EMAIL_UNAVAILABLE
                elif email_failure is 2:
                    clue_message = texts.EMAIL_LENGTH_OVER_255
                return render_with_clue_loginform_createform(request, 'authapp/main_first.html',
                                                             clue_message, LoginForm(), UserCreateForm(data))
            user_text_name_failure = user_text_name_failure_validate(name)
            if user_text_name_failure:
                clue_message = None
                if user_text_name_failure is 1:
                    clue_message = texts.USER_TEXT_NAME_LENGTH_PROBLEM
                return render_with_clue_loginform_createform(request, 'authapp/main_first.html',
                                                             clue_message, LoginForm(), UserCreateForm(data))

            return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                         None, LoginForm(), UserCreateForm(data))

            #######################################################################

        elif request.POST['type'] == 'create_second':
            form = UserCreateForm(request.POST)

            name = form.data['name']
            username = form.data['username']
            email = form.data['email']
            password = form.data['password']
            password_confirm = form.data['password_confirm']

            data = {
                'name': name,
                'username': username,
                'email': email,
            }
            username = username.lower()

            # validating username and password

            user_username_exist = UserUsername.objects.filter(username=username).exists()
            if user_username_exist:
                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                             texts.USERNAME_ALREADY_USED, LoginForm(), UserCreateForm(data))

            username_failure = user_username_failure_validate(username)
            if username_failure:
                clue_message = None
                if username_failure is 1:
                    clue_message = texts.USERNAME_UNAVAILABLE
                elif username_failure is 2:
                    clue_message = texts.USERNAME_LENGTH_PROBLEM
                elif username_failure is 3:
                    clue_message = texts.USERNAME_8_CANNOT_DIGITS
                elif username_failure is 4:
                    clue_message = texts.USERNAME_BANNED

                return clue_json_response(0, clue_message)

            primary_email_exist = UserPrimaryEmail.objects.filter(email=email).exists()
            if primary_email_exist:
                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                             texts.EMAIL_ALREADY_USED, LoginForm(), UserCreateForm(data))

            email_failure = user_primary_email_failure_validate(email)
            if email_failure:
                clue_message = None
                if email_failure is 1:
                    clue_message = texts.EMAIL_UNAVAILABLE
                elif email_failure is 2:
                    clue_message = texts.EMAIL_LENGTH_OVER_255
                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                             clue_message, LoginForm(), UserCreateForm(data))

            user_text_name_failure = user_text_name_failure_validate(name)
            if user_text_name_failure:
                clue_message = None
                if user_text_name_failure is 1:
                    clue_message = texts.USER_TEXT_NAME_LENGTH_PROBLEM
                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                             clue_message, LoginForm(), UserCreateForm(data))
            # password 조건
            password_failure = password_failure_validate(username, password, password_confirm)
            if password_failure:
                clue_message = None
                if password_failure is 1:
                    clue_message = texts.PASSWORD_NOT_THE_SAME
                elif password_failure is 2:
                    clue_message = texts.PASSWORD_LENGTH_PROBLEM
                elif password_failure is 3:
                    clue_message = texts.PASSWORD_EQUAL_USERNAME
                elif password_failure is 4:
                    clue_message = texts.PASSWORD_BANNED
                return render_with_clue_loginform_createform(request, 'authapp/main_second.html', clue_message,
                                                             LoginForm(), UserCreateForm(data))

            # Then, go to is_valid below
            if form.is_valid():
                new_user_create = None

                new_name = form.cleaned_data['name']
                new_username = form.cleaned_data['username']
                new_password = form.cleaned_data['password']
                new_email = form.cleaned_data['email']
                new_username = new_username.lower()
                try:
                    with transaction.atomic():

                        checker_username_result = 0
                        counter_username = 0
                        while checker_username_result is 0:
                            if counter_username <= 9:
                                try:
                                    id_number = make_id()
                                    new_user_create = User.objects.create_user(
                                        username=id_number,
                                        password=new_password,
                                        is_active=True,
                                    )

                                except IntegrityError as e:
                                    if 'UNIQUE constraint' in str(e.args):
                                        counter_username = counter_username + 1
                                    else:
                                        return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                                                     texts.CREATING_USER_EXTRA_ERROR, LoginForm(),
                                                                                     UserCreateForm(data))
                            else:
                                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                                             texts.CREATING_USER_EXTRA_ERROR, LoginForm(),
                                                                             UserCreateForm(data))
                            checker_username_result = 1

                        new_user_primary_email_create = UserPrimaryEmail.objects.create(
                            user=new_user_create,
                            email=new_email,
                            is_permitted=False,
                        )

                        new_user_username = UserUsername.objects.create(
                            user=new_user_create,
                            username=new_username,
                        )
                        new_user_text_name = UserTextName.objects.create(
                            user=new_user_create,
                            name=new_name
                        )
                        new_user_photo = UserPhoto.objects.create(
                            user=new_user_create,
                        )

                        birthday = str(form.cleaned_data['year']) + '-' + str(
                            form.cleaned_data['month']) + '-' + str(form.cleaned_data['day'])

                        new_user_birthday = UserBirthday.objects.create(
                            user=new_user_create,
                            birthday=birthday
                        )
                        new_user_gender = UserGender.objects.create(
                            user=new_user_create,
                            gender=form.cleaned_data['gender']
                        )
                        # 여기 기본적인 릴레이션 모델
                        new_following_count = FollowingCount.objects.create(user=new_user_create)
                        new_follower_count = FollowerCount.objects.create(user=new_user_create)
                        new_notice_count = NoticeCount.objects.create(user=new_user_create)

                except Exception:
                    return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                             texts.CREATING_USER_EXTRA_ERROR, LoginForm(),
                                                             UserCreateForm(data))

                checker_while_loop = 0
                counter_if_loop = 0
                uid = urlsafe_base64_encode(force_bytes(new_user_create.pk)).decode()
                token = account_activation_token.make_token(new_user_create)
                while checker_while_loop is 0:
                    if counter_if_loop <= 9:

                        try:

                            UserPrimaryEmailAuthToken.objects.create(
                                user_primary_email=new_user_primary_email_create,
                                uid=uid,
                                token=token,
                                email=new_email,
                            )
                        except IntegrityError as e:
                            if 'UNIQUE constraint' in str(e.args):
                                counter_if_loop = counter_if_loop + 1
                            else:
                                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                                             texts.EMAIL_CONFIRMATION_EXTRA_ERROR,
                                                                             LoginForm(),
                                                                             UserCreateForm(data))
                    checker_while_loop = 1

                subject = '[' + texts.SITE_NAME + ']' + texts.EMAIL_CONFIRMATION_SUBJECT

                message = render_to_string('authapp/_account_activation_email.html', {
                    'username': new_user_username.username,
                    'name': new_user_text_name.name,
                    'email': new_user_primary_email_create.email,
                    'domain': texts.SITE_DOMAIN,
                    'site_name': texts.SITE_NAME,
                    'uid': uid,
                    'token': token,
                })

                new_user_email_list = [new_email]

                send_mail(
                    subject=subject, message=message, from_email=options.DEFAULT_FROM_EMAIL,
                    recipient_list=new_user_email_list
                )
                # End Transaction

                login(request, new_user_create)
                ####################################################
                ####################################################
                return redirect(reverse('baseapp:user_main', kwargs={'user_username': new_user_username.username}))
            else:
                # 여기 로그인 된 경우 작업 해야 한다. 자동으로 기본화면으로 넘어가도록 하라.
                return render_with_clue_loginform_createform(request, 'authapp/main_second.html',
                                                             texts.CREATING_USER_EXTRA_ERROR, LoginForm(),
                                                             UserCreateForm(data))

        elif request.POST['type'] == 'log_in':

            form = LoginForm(request.POST)
            username = form.data['username']
            data = {
                'username': username,
            }

            if '@' in username:
                try:
                    user_primary_email = UserPrimaryEmail.objects.get(email=username, primary=True)
                except UserPrimaryEmail.DoesNotExist:
                    user_primary_email = None

                if user_primary_email is None:
                    return render_with_clue_loginform_createform_log_in(request, 'authapp/main_first.html',
                                                                 texts.LOGIN_EMAIL_NOT_EXIST, LoginForm(data),
                                                                 UserCreateForm(data))

            else:
                try:
                    user_username = UserUsername.objects.get(username=username)
                except UserUsername.DoesNotExist:
                    user_username = None

                if user_username is None:
                    return render_with_clue_loginform_createform_log_in(request, 'authapp/main_first.html',
                                                                 texts.LOGIN_USERNAME_NOT_EXIST, LoginForm(data),
                                                                 UserCreateForm())

            if form.is_valid():

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)

                if user is not None:

                    try:
                        user_delete = UserDelete.objects.get(user=user)
                    except UserDelete.DoesNotExist:
                        user_delete = None
                    if user_delete is not None:
                        user_delete.delete()
                    if user.is_active is False:
                        user.is_active = True
                        user.save()
                    login(request, user)

                    ####################################################
                    ####################################################
                    return redirect(reverse('baseapp:main_create_log_in'))

                else:
                    data = {
                        'username': username,
                    }
                    return render_with_clue_loginform_createform_log_in(request, 'authapp/main_first.html',
                                                                 texts.LOGIN_FAILED, LoginForm(data),
                                                                 UserCreateForm())

    else:
        if request.user.is_authenticated:
            return render(request, 'baseapp/user_home.html')
        return render_with_clue_loginform_createform(request, 'authapp/main_first.html', None, LoginForm(), UserCreateForm())


def log_out(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse('baseapp:main_create_log_in'))
    else:
        logout(request)
        return redirect(reverse('baseapp:main_create_log_in'))


def primary_email_key_confirm(request, uid, token):
    if request.method == "GET":
        try:
            with transaction.atomic():
                try:
                    user_primary_email_auth_token = UserPrimaryEmailAuthToken.objects.get(uid=uid, token=token)
                except UserPrimaryEmailAuthToken.DoesNotExist:
                    clue = {'message': texts.KEY_UNAVAILABLE}
                    return render(request, 'authapp/primary_email_key_confirm.html', {'clue': clue})

                if user_primary_email_auth_token is None \
                        or ((now() - user_primary_email_auth_token.created) > timedelta(seconds=60*10)) \
                        or not (UserPrimaryEmailAuthToken.objects.filter(
                            user_primary_email=user_primary_email_auth_token.user_primary_email
                        ).last() == user_primary_email_auth_token):
                    clue = {'message': texts.KEY_EXPIRED}
                    return render(request, 'authapp/primary_email_key_confirm.html', {'clue': clue})

                try:
                    uid = force_text(urlsafe_base64_decode(uid))
                    user = User.objects.get(pk=uid)
                    user_primary_email = user_primary_email_auth_token.user_primary_email
                except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    user = None
                    user_primary_email = None

                if user is None or user_primary_email is None:
                    clue = {'message': texts.KEY_EXPIRED}
                    return render(request, 'authapp/primary_email_key_confirm.html', {'clue': clue})

                # 만약 그 사이에 누군가 UserVerifiedEmail 등록해버렸다면 그 때 primary 이메일도 삭제할 것이므로 괜찮다.
                # 결국 이 전에 return 되어 여기까지 오지도 않을 것이다.
                user_primary_email.email = user_primary_email_auth_token.email
                user_primary_email.is_permitted = True
                user_primary_email.save()

                user.save()

                clue = {'message': texts.KEY_CONFIRM_SUCCESS, 'success': 'got succeed', }
                return render(request, 'authapp/primary_email_key_confirm.html', {'clue': clue})
        except Exception:
            clue = {'message': texts.KEY_OVERALL_FAILED}
            return render(request, 'authapp/primary_email_key_confirm.html', {'clue': clue})


def password_change(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                username = request.user.userusername.username
                user = authenticate(username=username, password=form.cleaned_data['password'])
                if user is not None:
                    new_password = form.cleaned_data['new_password']
                    new_password_confirm = form.cleaned_data['new_password_confirm']
                    # password 조건
                    password_failure = password_failure_validate(username, new_password, new_password_confirm)
                    if password_failure:
                        clue_message = None
                        if password_failure is 1:
                            clue_message = texts.PASSWORD_NOT_THE_SAME
                        elif password_failure is 2:
                            clue_message = texts.PASSWORD_LENGTH_PROBLEM
                        elif password_failure is 3:
                            clue_message = texts.PASSWORD_EQUAL_USERNAME
                        elif password_failure is 4:
                            clue_message = texts.PASSWORD_BANNED
                        return render_with_clue_one_form(request, 'authapp/password_change.html',
                                                         clue_message, PasswordChangeForm())
                    try:
                        with transaction.atomic():

                            user.set_password(new_password)
                            user.save()
                            update_session_auth_hash(request, request.user)
                            return render_with_clue_one_form(request, 'authapp/password_change_complete.html', texts.PASSWORD_CHANGED,
                                                             PasswordChangeForm())
                    except Exception:
                        return render_with_clue_one_form(request, 'authapp/password_change.html', texts.UNEXPECTED_ERROR,
                                                         PasswordChangeForm())

                else:
                    return render_with_clue_one_form(request, 'authapp/password_change.html', texts.PASSWORD_AUTH_FAILED, PasswordChangeForm())
            else:
                return render_with_clue_one_form(request, 'authapp/password_change.html', texts.PASSWORD_AUTH_FAILED, PasswordChangeForm())
        else:
            return redirect(reverse('baseapp:main_create_log_in'))

    else:
        if request.user.is_authenticated:
            return render_with_clue_one_form(request, 'authapp/password_change.html', None, PasswordChangeForm())
        else:
            return redirect(reverse('baseapp:main_create_log_in'))


def password_reset(request):
    if request.method == "POST":

        form = PasswordResetForm(request.POST)

        username = form.data['username']
        if '@' in username:
            try:
                user_primary_email = UserPrimaryEmail.objects.get(email=username)
            except UserPrimaryEmail.DoesNotExist:
                return render_with_clue_one_form(request, 'authapp/password_reset.html', texts.LOGIN_EMAIL_NOT_EXIST, PasswordResetForm())
            user = user_primary_email.user

        else:
            try:
                user_username = UserUsername.objects.get(username=username)
            except UserUsername.DoesNotExist:
                return render_with_clue_one_form(request, 'authapp/password_reset.html', texts.LOGIN_USERNAME_NOT_EXIST, PasswordResetForm())
            user = user_username.user
            user_primary_email = UserPrimaryEmail.objects.get(email=user.userprimaryemail.email)

        checker_while_loop = 0
        counter_if_loop = 0
        uid = None
        token = None

        while checker_while_loop is 0:
            if counter_if_loop <= 9:

                try:
                    uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
                    token = account_activation_token.make_token(user)
                    UserPasswordResetToken.objects.create(
                        user_primary_email=user_primary_email,
                        uid=uid,
                        token=token,
                        email=user_primary_email.email,
                    )

                except IntegrityError as e:
                    if 'UNIQUE constraint' in str(e.args):
                        counter_if_loop = counter_if_loop + 1
                    else:
                        return render_with_clue_one_form(request, 'authapp/password_reset.html',
                                                         texts.UNEXPECTED_ERROR, PasswordResetForm())
            checker_while_loop = 1

        # Send Email
        subject = '[' + texts.SITE_NAME + ']' + texts.PASSWORD_RESET_SUBJECT

        message = render_to_string('authapp/_password_reset_email.html', {
            'username': user.userusername.username,
            'name': user.usertextname.name,
            'email': user_primary_email.email,
            'domain': texts.SITE_DOMAIN,
            'site_name': texts.SITE_NAME,
            'uid': uid,
            'token': token,
        })

        email_list = [user_primary_email.email]

        send_mail(
            subject=subject, message=message, from_email=options.DEFAULT_FROM_EMAIL,
            recipient_list=email_list
        )
        # user_primary_email.email
        return render(request, 'authapp/password_reset_email_sent.html')

    else:
        return render_with_clue_one_form(request, 'authapp/password_reset.html', None, PasswordResetForm())


def password_reset_key_confirm(request, uid, token):
    if request.method == "GET":
        try:
            user_password_reset_token = UserPasswordResetToken.objects.get(uid=uid, token=token)
        except UserPasswordResetToken.DoesNotExist:
            clue = {'message': texts.KEY_UNAVAILABLE}
            return render(request, 'authapp/password_reset_key_confirm_error.html', {'clue': clue})

        if user_password_reset_token is None \
                or ((now() - user_password_reset_token.created) > timedelta(seconds=60 * 10)) \
                or not (UserPasswordResetToken.objects.filter(
                user_primary_email=user_password_reset_token.user_primary_email
                ).last() == user_password_reset_token):
            clue = {'message': texts.KEY_EXPIRED}
            return render(request, 'authapp/password_reset_key_confirm_error.html', {'clue': clue})

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            user_primary_email = user_password_reset_token.user_primary_email
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            user_primary_email = None

        if user is None or user_primary_email is None:
            clue = {'message': texts.KEY_EXPIRED}
            return render(request, 'authapp/password_reset_key_confirm_error.html', {'clue': clue})

        # 이러면 비밀번호 새로 입력할 창을 준다.
        form = PasswordResetConfirmForm()

        return render(request, 'authapp/password_reset_key_confirmed_and_reset.html', {'form': form})

    # 여기선 새 패스워드 값을 받아서 처리한다.
    elif request.method == "POST":
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            new_password_confirm = form.cleaned_data['password_confirm']

            try:
                with transaction.atomic():
                    try:
                        user_password_reset_token = UserPasswordResetToken.objects.get(uid=uid, token=token)
                    except UserPasswordResetToken.DoesNotExist:
                        clue = {'message': texts.KEY_UNAVAILABLE}
                        return render(request, 'authapp/password_reset_key_confirm_error.html', {'clue': clue})

                    if user_password_reset_token is None \
                            or ((now() - user_password_reset_token.created) > timedelta(seconds=60 * 10)) \
                            or not (UserPasswordResetToken.objects.filter(
                            user_primary_email=user_password_reset_token.user_primary_email
                            ).last() == user_password_reset_token):
                        clue = {'message': texts.KEY_EXPIRED}
                        return render(request, 'authapp/password_reset_key_confirm_error.html', {'clue': clue})

                    try:
                        uid = force_text(urlsafe_base64_decode(uid))
                        user = User.objects.get(pk=uid)
                        user_primary_email = user_password_reset_token.user_primary_email
                    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                        user = None
                        user_primary_email = None

                    if user is None or user_primary_email is None:
                        clue = {'message': texts.KEY_EXPIRED}
                        return render(request, 'authapp/password_reset_key_confirm_error.html', {'clue': clue})

                    password_failure = password_failure_validate(user.userusername.username,
                                                                 new_password,
                                                                 new_password_confirm)
                    if password_failure:
                        clue_message = None
                        if password_failure is 1:
                            clue_message = texts.PASSWORD_NOT_THE_SAME
                        elif password_failure is 2:
                            clue_message = texts.PASSWORD_LENGTH_PROBLEM
                        elif password_failure is 3:
                            clue_message = texts.PASSWORD_EQUAL_USERNAME
                        elif password_failure is 4:
                            clue_message = texts.PASSWORD_BANNED
                        return render_with_clue_one_form(request, 'authapp/password_reset_key_confirmed_and_reset.html',
                                                         clue_message, PasswordResetConfirmForm())
                    user.set_password(new_password)
                    user.save()

                    user_primary_email.is_permitted = True
                    user_primary_email.save()
                    update_session_auth_hash(request, user)
                    return render(request, 'authapp/password_reset_completed.html')

            except Exception:
                return render_with_clue_one_form(request, 'authapp/password_reset_key_confirm_error.html',
                                                 texts.UNEXPECTED_ERROR, PasswordChangeForm())


def deactivate_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            form = PasswordCheckBeforeDeactivationForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.user.userusername.username,
                                    password=form.cleaned_data['password'])
                if user is not None:
                    try:
                        with transaction.atomic():
                            user.is_active = False
                            user.save()
                            logout(request)
                            return render(request, 'authapp/deactivate_user_done.html')
                    except Exception:
                        return render_with_clue_one_form(request, 'authapp/deactivate_user.html',
                                                         texts.UNEXPECTED_ERROR,
                                                         PasswordCheckBeforeDeactivationForm())
                else:
                    return render_with_clue_one_form(request, 'authapp/deactivate_user.html', texts.PASSWORD_AUTH_FAILED, PasswordCheckBeforeDeactivationForm())
            else:
                return render_with_clue_one_form(request, 'authapp/deactivate_user.html', texts.PASSWORD_AUTH_FAILED,
                                                 PasswordCheckBeforeDeactivationForm())
        else:
            return redirect(reverse('baseapp:main_create_log_in'))
    else:
        if request.user.is_authenticated:
            form = PasswordCheckBeforeDeactivationForm()
            return render(request, 'authapp/deactivate_user.html', {'form': form})
        else:
            return redirect(reverse('baseapp:main_create_log_in'))


def delete_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            form = PasswordCheckBeforeDeleteForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.user.userusername.username,
                                    password=form.cleaned_data['password'])

                if user is not None:
                    try:
                        with transaction.atomic():
                            UserDelete.objects.create(user=user)
                            user.is_active = False
                            user.save()
                            logout(request)
                            return render(request, 'authapp/delete_user_done.html')
                    except Exception:
                        return render_with_clue_one_form(request, 'authapp/delete_user.html', texts.UNEXPECTED_ERROR, PasswordCheckBeforeDeleteForm())
                else:
                    return render_with_clue_one_form(request, 'authapp/delete_user.html', texts.PASSWORD_AUTH_FAILED, PasswordCheckBeforeDeleteForm())
            else:
                return render_with_clue_one_form(request, 'authapp/delete_user.html', texts.PASSWORD_AUTH_FAILED,
                                                 PasswordCheckBeforeDeleteForm())
        else:
            return redirect(reverse('baseapp:main_create_log_in'))
    else:
        if request.user.is_authenticated:
            form = PasswordCheckBeforeDeleteForm()
            return render(request, 'authapp/delete_user.html', {'form': form})
        else:
            return redirect(reverse('baseapp:main_create_log_in'))


def settings(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'authapp/settings.html')
        else:
            return redirect(reverse('baseapp:main_create_log_in'))

def settings_other(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'authapp/settings_other.html')
        else:
            return redirect(reverse('baseapp:main_create_log_in'))

@ensure_csrf_cookie
def email_ask(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():

                if request.POST.get('type', None) is None:
                    return JsonResponse({'res': 2})
                elif request.POST.get('type', None) == 'close':
                    try:
                        request.user.userprimaryemail.save()
                    except Exception:
                        return JsonResponse({'res': 0})
                    return JsonResponse({'res': 1})
                elif request.POST.get('type', None) == 'ask':
                    request.user.userprimaryemail.save()
                    if (now() - request.user.userprimaryemail.updated) > timedelta(seconds=60 * 60 * 4):
                        return JsonResponse({'res': 1})
                    else:
                        return JsonResponse({'res': 0})
        return JsonResponse({'res': 2})


'''

'''
def crop(request):
    if request.method == "GET":

        form = TestPicForm()

        testphoto = TestPic.objects.all().last()

        return render(request, 'authapp/crop.html', {'form': form, 'testphoto': testphoto})
    else:
        if request.is_ajax():
            testpic = TestPic.objects.get(pk=1)

            form = TestPicForm(request.POST, request.FILES, instance=testpic)
            if form.is_valid():

                DJANGO_TYPE = request.FILES['file'].content_type

                if DJANGO_TYPE == 'image/jpeg':
                    PIL_TYPE = 'jpeg'
                    FILE_EXTENSION = 'jpg'
                elif DJANGO_TYPE == 'image/png':
                    PIL_TYPE = 'png'
                    FILE_EXTENSION = 'png'
                    # DJANGO_TYPE == 'image/gif
                elif DJANGO_TYPE == 'image/gif':
                    return JsonResponse({'res':0})

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
                image = Image.open(BytesIO(request.FILES['file'].read()))
                image_modified = image.rotate(-1*rotate, expand=True).crop((x, y, x+width, y+height))
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
                testpic.file.save(
                    '%s_300px.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
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
                testpic.file_50.save(
                    '%s_50px.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                    suf, save=True)

                return JsonResponse({'success': 'file_uploaded with: ' + 'on form_valid', 'url': 'maybe'})
            return JsonResponse({'success': 'file_uploaded with: ' + 'failed form_valid'})


# form.save()
def crop_request_file(request_file, x, y, width, height, resize_width, resize_height):
    from PIL import Image
    from io import BytesIO
    read_file = BytesIO(request_file.read())
    image = Image.open(read_file)
    image = image.crop((x, y, x+width, y+height))
    image = image.resize((resize_width, resize_height), Image.ANTIALIAS)
    image_file = BytesIO()
    image.save(image_file, 'JPEG')
    request_file.file = image_file
    return request_file


'''
                from PIL import Image
                from io import BytesIO
                # form.save()

                data = request.FILES['file']
                print('1')
                input_file = BytesIO(data.read())
                image_crop = Image.open(input_file)
                print('2')
                data.seek(0)
                print('3')
                image_crop = image_crop.crop((1, 1, 100, 100))
                print('4')
                image_resize = image_crop.resize((300, 300), Image.ANTIALIAS)

                image_file = BytesIO()
                image_resize.save(image_file, 'JPEG')

                data.file = image_file
                testpic.file = data

                testpic.save()
                print('3')
                data.seek(0)

                data = request.FILES['file']
                input_file = BytesIO(data.read())
                input_file = input_file.name
                image_crop = Image.open(input_file)
                image_crop = image_crop.crop((40, 40, 140, 140))
                image_resize = image_crop.resize((50, 50), Image.ANTIALIAS)
                image_file = BytesIO()
                image_resize.save(image_file, 'JPEG')
                data.file = image_file
                testpic.file_50 = data
                testpic.save()
                '''
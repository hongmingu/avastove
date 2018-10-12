from django.contrib.sites.shortcuts import get_current_site

BAD_ACCESS = 'Bad Access'
UNEXPECTED_ERROR = 'unexpected error'

USER_TEXT_NAME_LENGTH_PROBLEM = 'name should be 6 <= password <= 30 /' \
                          ' greater than or equal to 6, less than or equal to 30'
USER_TEXT_NAME_BANNED = 'It\'s unavailable name'
USER_TEXT_NAME_CHANGED = 'name is changed'

USERNAME_UNAVAILABLE = 'username can be made of digit, alphabet, . or _'
USERNAME_LENGTH_PROBLEM = 'username should be 6 <= password <= 30 /' \
                          ' greater than or equal to 6, less than or equal to 30'
USERNAME_ALREADY_USED = 'This username is already used'
USERNAME_BANNED = 'It\'s unavailable username'
USERNAME_8_CANNOT_DIGITS = 'If username length is greater than or equal to 8, cannot be made of only digits'
USERNAME_CHANGED = 'username is changed'

EMAIL_UNAVAILABLE = 'It\'s unavailable email'
EMAIL_LENGTH_OVER_255 = 'You have to change email length'
EMAIL_ALREADY_USED = 'This email is already used'
EMAIL_CONFIRMATION_EXTRA_ERROR = 'email confirmation goes wrong'
EMAIL_CONFIRMATION_SUBJECT = 'Email confirmation to activate your account'
EMAIL_ADDED_SENT = 'email has added, confirm your email'
EMAIL_SENT = 'email has been sent, confirm your email'
EMAIL_NOT_EXIST = 'There is no email like that'
EMAIL_PRIMARY_CANNOT_BE_REMOVED = 'Primary email cannot be removed'
EMAIL_CANNOT_SEND = 'cannot send confirmation to this email'
EMAIL_DELETED = 'email is removed'
EMAIL_ALREADY_PRIMARY = 'email is already primary'
EMAIL_GET_PRIMARY = 'email got primary'

PASSWORD_NOT_THE_SAME = 'both passwords you submitted are not the same'
PASSWORD_LENGTH_PROBLEM = 'password should be 6 <= password <= 128 /' \
                          ' greater than or equal to 6, less than or equal to 128'
PASSWORD_EQUAL_USERNAME = 'password cannot be the same as username'
PASSWORD_BANNED = 'It\'s unavailable password'
PASSWORD_AUTH_FAILED = 'password auth has failed'
PASSWORD_RESET_SUBJECT = 'Password reset email'
PASSWORD_CHANGED = 'Password has been changed'

CREATING_USER_EXTRA_ERROR = 'There is something wrong on creating user'
CREATING_EMAIL_EXTRA_ERROR = 'There is something wrong on adding email'
CREATING_USER_OVERALL_ERROR = 'There is something wrong'

RECAPTCHA_CONFIRM_NEED = 'Check that you are human'

KEY_UNAVAILABLE = 'This key is unavailable'
KEY_EXPIRED = 'This key is expired'
KEY_ALREADY_VIEWED = 'This key is already expired'
KEY_CONFIRM_SUCCESS = 'Thanks for email confirmation'
KEY_OVERALL_FAILED = 'There is something wrong for key'

LOGIN_FAILED = 'Login has failed'
LOGIN_EMAIL_NOT_EXIST = 'Email does not exist'
LOGIN_USERNAME_NOT_EXIST = 'Username does not exist'

SITE_NAME = 'ChatKaboo'
SITE_DOMAIN = 'www.chatkaboo.com'
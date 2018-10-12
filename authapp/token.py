from django.utils import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.timezone import now


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(now()) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()

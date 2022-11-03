import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from util.constants import EMAIL_REGEXP_CPL
from util.constants import PHONE_REGEXP_CPL


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # cancel op if fields not provided
        if username is None or password is None:
            return

        # verifies if username is phone, email, or default matricule
        if re.fullmatch(PHONE_REGEXP_CPL, username):
            kwargs = {'telephone': username}
        elif re.fullmatch(EMAIL_REGEXP_CPL, username):
            kwargs = {'email': username}
        else:
            kwargs = {'matricule': username}

        # tries to get user from provided data
        auth_user = get_user_model().objects.get(**kwargs)
        return (
            auth_user
            if auth_user.check_password(password)
            and self.user_can_authenticate(auth_user)
            else None
        )

    def user_can_authenticate(self, auth_user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return auth_user.user.is_active

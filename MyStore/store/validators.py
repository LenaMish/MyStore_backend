from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_unique_username(username):
    user = User.objects.filter(username=username).first()
    if user:
        raise ValidationError(
            _('%(value)s is already exists'),
            params={'value': username},
        )
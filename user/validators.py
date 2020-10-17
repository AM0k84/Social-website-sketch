from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# todo: DOROBIC WALIDATORY DO HASLA, USERA, ITP
class Numeric1PasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('Your password can’t be entirely numeric.')

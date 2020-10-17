from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


# from user.models import Profile


class SignUpForm(UserCreationForm):
    username = UsernameField(label=_("Nazwa użytkownika"), widget=forms.TextInput(), )
    email = forms.EmailField(max_length=254, label="E-mail", widget=forms.EmailInput(), validators=[EmailValidator])
    checkbox = forms.BooleanField(label="Zaakceptuj regulamin", required=True)

    class Meta:
        # model = locate(settings.AUTH_USER_MODEL)
        # model = Profile
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", 'checkbox',)

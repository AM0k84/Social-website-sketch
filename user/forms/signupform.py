from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


# from user.models import Profile


class SignUpForm(UserCreationForm):
    username = UsernameField(label=_("Nazwa użytkownika"), widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}) )
    email = forms.EmailField(max_length=254, label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}), validators=[EmailValidator])
    checkbox = forms.BooleanField(label="Zaakceptuj regulamin", required=True)

    class Meta:
        # model = locate(settings.AUTH_USER_MODEL)
        # model = Profile
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", 'checkbox',)

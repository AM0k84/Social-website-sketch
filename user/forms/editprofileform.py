from django import forms

from user.models import Profile


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Imię",
        max_length=150,
        help_text="Twoje imię",
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=False,
    )

    last_name = forms.CharField(
        label="Nazwisko",
        max_length=150,
        help_text="Twoje nazwisko",
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}),
        required=False,
    )

    photo = forms.ImageField(
        label="Zdjęcie",
        help_text="Akceptowane pliki to: jpg....",
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control form-control pr-3 shadow p-1 mb-1 bg-white rounded"}), required=False,
    )

    bio = forms.CharField(
        label="Bio",
        max_length=500,
        help_text="Krótka biografia",
        widget=forms.Textarea(attrs={"class": "form-control form-control-lg pr-5 shadow p-1 mb-1 bg-white rounded"}), required=False
    )

    website_url = forms.URLField(
        label="Strona internetowa",
        max_length=500,
        help_text="Twoja strona internetowa",
        widget=forms.URLInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"}),
        required=False,
    )

    # todo: W PRZYSZŁOŚCI ZMIANĘ EMAILA ZROBIĆ W USTAWIENIACH RAZEM ZE ZMIANĄ HASŁA LUB PO PROSTU W INNY BARDZIEJ PROFESJONALNY SPOSOB
    email = forms.EmailField(
        label="E-mail",
        max_length=500,
        help_text="Twój adres email",
        widget=forms.EmailInput(attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"})
    )

    facebook_url = forms.URLField(
        label="Facebook",
        max_length=500,
        help_text="Twój Facebook",
        widget=forms.URLInput(
            attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"}), required=False,

    )

    instagram_url = forms.URLField(
        label="Instagram",
        max_length=500,
        help_text="Twój Instagram",
        widget=forms.URLInput(
            attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"}), required=False,
    )

    soundcloud_url = forms.URLField(
        label="Soundcloud",
        max_length=500,
        help_text="Twój Soundcloud",
        widget=forms.URLInput(
            attrs={"class": "form-control form-control-lg pr-5 shadow p-2 mb-1 bg-white rounded"}), required=False,
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'photo', 'bio', 'website_url', 'facebook_url', 'instagram_url',
                  'soundcloud_url']

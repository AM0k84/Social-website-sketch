from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView

from hitcount.views import HitCountDetailView

from news.models import Article
from user.forms.signupform import SignUpForm
from user.models import Profile
from video.models import Video


# todo: POPRAWIC REJESTRACJE I LOGOWANIE UZYTKOWNIKA
# todo:DOROBIC VALIDATORY I FORMULARZE MAJA SIE WYSWIETLAC W INNY SPOSOB - POMYSLEC


class LoginRequiredMixin(BaseLoginRequiredMixin):
    def get_login_url(self):
        return reverse("user:login")


class ProfileView(HitCountDetailView):
    model = Profile
    template_name = 'profile/profile.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_articles'] = Article.objects.filter(author__slug=self.kwargs['slug']).order_by('-pk')
        context['user_videos'] = Video.objects.filter(author__slug=self.kwargs['slug']).order_by('-pk')
        return context


# todo: przerobić na formularz w forms
class EditProfileInfoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'profile/edit_profile.html'
    fields = ['bio', 'photo', 'email', 'first_name', 'last_name', 'website_url', 'facebook_url', 'instagram_url',
              'soundcloud_url']

    def get_success_url(self):
        slug = self.kwargs['slug']
        messages.success(request=self.request, message="PROFIL ZOSTAŁ ZAKTUALIZOWANY")
        return reverse_lazy("profile", kwargs={'slug': slug})

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        # todo: DOROBIĆ MESSAGES JEŚLI PROBUJE SIĘ EDYTOWAC OBCY PROFIL
        return False


class RegisterView(CreateView):
    template_name = "auth/register.html"
    form_class = SignUpForm

    def form_valid(self, form):
        messages.success(request=self.request, message="PROFIL ZOSTAŁ POPRAWNIE UTWORZONY")
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self) -> str:
        return reverse("index")


class LoginView(View):
    template_name = "auth/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")

        return render(request, self.template_name, {})

    def post(self, request):
        username: str = request.POST.get("username")
        password: str = request.POST.get("password")

        user: User or None = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request=self.request, message="POPRAWNIE ZALOGOWANO")
            return redirect("index")
        messages.warning(request=self.request, message="BŁĘDNY LOGIN LUB HASŁO")
        return redirect("user:login")


def logout_view(request):
    logout(request)
    messages.success(request, message="POPRAWNIE WYLOGOWANO")
    return redirect("index")


class ChangePassword(FormView, LoginRequiredMixin):
    login_url = "/login"
    template_name = "auth/change_password.html"
    form_class = PasswordChangeForm

    def get_form(self):
        if self.request.POST:
            return self.form_class(self.request.user, self.request.POST)
        return self.form_class(self.request.user)

    def form_valid(self, form):
        messages.success(request=self.request, message="HASŁO ZMIENIONE PRAWIDŁOWO")
        form.save()
        return redirect(reverse('index'))

    def get_success_url(self) -> str:
        return reverse("index")

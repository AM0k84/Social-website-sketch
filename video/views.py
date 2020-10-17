import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from hitcount.views import HitCountDetailView


from video.forms import EditVideoForm, AddVideoForm, VideoCommentForm
from video.models import Video, VideoCategory, VideoComment


class LoginRequiredMixin(BaseLoginRequiredMixin):
    def get_login_url(self):
        #todo: DODAĆ MESSAGE ŻE NAJPIERW TRZEBA SIĘ ZALOGOWAĆ.
        return reverse("user:login")


class AddVideo(LoginRequiredMixin, CreateView):
    model = Video
    template_name = 'video/add_video.html'
    form_class = AddVideoForm

    # FUNKCJADZIEKI KTOREMU PRZEKAZUJEM ZALOGOWANEGO UZYTKOWNIKA DO FORMULARZA
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(request=self.request, message="VIDEO ZOSTAŁO POPRAWNIE DODANE")
        return super().form_valid(form)


# W TEMPLATE update_video.html USTAWIONE JEST ŻE KONKRETNY ARTYKUŁ MOŻE USUNĄĆ TYLKO JEGO WŁAŚCICIEL.
# W USUWANIU ARTYKUŁU ZROBIONE JEST TO SAMO ZA POMOCĄ MIXINA
class UpdateVideoView(LoginRequiredMixin, UpdateView):
    template_name = 'video/update_video.html'
    form_class = EditVideoForm
    model = Video

    def get_success_url(self):
        pk = self.kwargs["pk"]
        slug = self.kwargs['slug']
        messages.success(request=self.request, message="VIDEO ZOSTAŁO POPRAWNIE ZAKTUALIZOWANE")
        return reverse_lazy("video:video_detail", kwargs={'pk': pk, 'slug': slug})


# ZA POMOCĄ UserPassesTestMixin SPRAWDZAM CZY NEWS KTORY JEST USUWANY NALEŻY DO AUTORA NEWSA
# DZIĘKI TEMU NIE BĘDZIE MÓGŁ USUNĄĆ NEWSA JEŚLI NIE JEST JEGO AUTOREM
# NAWET JEŚLI ZNA KONKRETNY URL DO JEGO USUNIĘCIA
class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'video/delete_video.html'

    # SPRAWDZA CZY ZALOGOWANY USER TO AUTOR POSTA KTÓRY CHCE USUNĄĆ
    def test_func(self):
        video = self.get_object()
        if self.request.user == video.author:
            return True
        return False

    def get_success_url(self):
        # todo: W PRZYSZŁOŚCI DODAĆ INNE PRZEKIEROWANIE -> NA WSZYSTKIE VIDEO USERA
        messages.success(request=self.request, message="VIDEO ZOSTAŁO USUNIĘTE")
        return reverse_lazy('video:all_videos_list')


class AllVideosListView(ListView):
    template_name = 'video/videos_list.html'
    model = Video
    queryset = Video.objects.order_by('-pk')
    paginate_by = 5


class VideoDetailView(FormMixin, HitCountDetailView):
    template_name = 'video/video_detail.html'
    model = Video
    count_hit = True
    form_class = VideoCommentForm


    def get_success_url(self):
        pk = self.kwargs["pk"]
        slug = self.kwargs['slug']
        return reverse_lazy('video:video_detail', kwargs={'pk': pk, 'slug': slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = VideoComment.objects.filter(video_id=self.object.id).all()
        page = self.request.GET.get('page')
        # ustawienie paginacji komentarzy
        context['comments'] = Paginator(queryset, 2).get_page(page)
        context['comments_number'] = VideoComment.objects.filter(video_id=self.object.id).count()
        context['form'] = VideoCommentForm()
        return context

    def form_valid(self, form):
        form.instance.video = self.object
        form.instance.author = self.request.user
        form.save()
        messages.success(request=self.request, message="KOMENTARZ ZOSTAŁ DODANY POPRAWNIE")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CategoryVideoList(ListView):
    template_name = 'video/category_videos_list.html'
    model = Video
    queryset = Video.objects.order_by('-pk')
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            category__slug=self.kwargs['slug']
        )

    def videocategory(self):
        return get_object_or_404(VideoCategory, slug=self.kwargs['slug'])



# NA CHWILĘ OBECNĄ POKAZUJĘ WSZYSTKIE POPULARNE Z OSTATNICH MINUT (NAJWIĘCEJ WYŚWIETLEŃ W OSTANIE 10 MIN)
# todo: ZROBIĆ NAJPOPULARNIEJSZE Z 24H, TYGODNIA, MIESIĄCA
class MostPopularVideosListView(ListView):
    template_name = 'video/trending_videos.html'
    model = Video

    # TO QUERY POKAZUJE NAM LISTE NEWSÓW Z NAJWIĘKSZĄ ILOŚCIĄ WYŚWIETLEŃ Z OSTATNICH 10 MIN
    # MAXYMALNIE 20 NEWSÓW
    def get_queryset(self):
        period = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=10)
        return self.model.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:20]


#wszystkie promowane
class PromotedVideosView(ListView):
    model = Video
    template_name = 'video/promoted_videos.html'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.all().order_by('-pk').filter(is_promoted=True)


#kozaki
#todo: W PRZYSZŁOŚCI BARDZIEJ SKOMPLIKOWANY FILTER HOT NEWSÓW
class MostPopularPromotedVideosView(ListView):
    model = Video
    template_name = 'video/hot_videos.html'

    def get_queryset(self):
        period = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=10)
        return self.model.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts').filter(is_promoted=True)[:20]
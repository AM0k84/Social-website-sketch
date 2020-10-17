import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin

from hitcount.views import HitCountDetailView
from news.forms import AddArticleForm, CommentForm, EditArticleForm
from news.models import Article, ArticleCategory, ArticleComment


class LoginRequiredMixin(BaseLoginRequiredMixin):
    def get_login_url(self):
        # todo: DODAĆ MESSAGE ŻE NAJPIERW TRZEBA SIĘ ZALOGOWAĆ.
        return reverse("user:login")


class AddArticle(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'news/add_article.html'
    form_class = AddArticleForm

    # FUNKCJADZIEKI KTOREMU PRZEKAZUJEM ZALOGOWANEGO UZYTKOWNIKA DO FORMULARZA
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(request=self.request, message="NEWS ZOSTAŁ DODANY")
        return super().form_valid(form)


# W TEMPLATE update_article.html USTAWIONE JEST ŻE KONKRETNY ARTYKUŁ MOŻE USUNĄĆ TYLKO JEGO WŁAŚCICIEL.
# W USUWANIU ARTYKUŁU ZROBIONE JEST TO SAMO ZA POMOCĄ MIXINA
class UpdateArticleView(LoginRequiredMixin, UpdateView):
    template_name = 'news/update_article.html'
    form_class = EditArticleForm
    model = Article

    def get_success_url(self):
        pk = self.kwargs["pk"]
        slug = self.kwargs['slug']
        messages.success(request=self.request, message="NEWS ZOSTAŁ POPRAWNIE ZAKTUALIZOWANY")
        return reverse_lazy("news:article_detail", kwargs={'pk': pk, 'slug': slug})


# ZA POMOCĄ UserPassesTestMixin SPRAWDZAM CZY NEWS KTORY JEST USUWANY NALEŻY DO AUTORA NEWSA
# DZIĘKI TEMU NIE BĘDZIE MÓGŁ USUNĄĆ NEWSA JEŚLI NIE JEST JEGO AUTOREM
# NAWET JEŚLI ZNA KONKRETNY URL DO JEGO USUNIĘCIA
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'news/delete_article.html'

    # SPRAWDZA CZY ZALOGOWANY USER TO AUTOR POSTA KTÓRY CHCE USUNĄĆ
    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False

    def get_success_url(self):
        # todo: W PRZYSZŁOŚCI DODAĆ INNE PRZEKIEROWANIE -> NA WSZYSTKIE NEWSY USERA
        messages.success(request=self.request, message="NEWS ZOSTAŁ USUNIĘTY")
        return reverse_lazy('news:all_articles_list')


class ArticleDetailView(FormMixin, HitCountDetailView):
    template_name = 'news/article_detail.html'
    model = Article
    count_hit = True
    form_class = CommentForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        slug = self.kwargs['slug']
        return reverse_lazy('news:article_detail', kwargs={'pk': pk, 'slug': slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = ArticleComment.objects.filter(article_id=self.object.id).all()
        page = self.request.GET.get('page')
        #ustawienie paginacji komentarzy
        context['comments'] = Paginator(queryset, 2).get_page(page)
        context['comments_number'] = ArticleComment.objects.filter(article_id=self.object.id).count()
        context['form'] = CommentForm()
        return context

    def form_valid(self, form):
        form.instance.article = self.object
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


#  W DetailView ZWRACA 1 OBIEKT W ZWIĄZKU Z TYM NIE MOGĘ ZROBIĆ PAGINACJI KOMENTARZY.
# DOTYCZY template 'category_article_list' DLA OBIEKTU (ArticleCategory)
# W TEMPLATE OBIEKTY Z DANEJ KATEGORII WYCIĄGANE SĄ ITERACYJNIE
# class CategoryArticlesList(DetailView):
#     template_name = 'news/category_articles_list.html'
#     model = ArticleCategory
class CategoryArticlesList(ListView):
    template_name = 'news/category_articles_list.html'
    model = Article
    queryset = Article.objects.order_by('-pk')
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            category__slug=self.kwargs['slug'])

    def articlecategory(self):
        return get_object_or_404(ArticleCategory, slug=self.kwargs['slug'])


class AllArticlesListView(ListView):
    template_name = 'news/articles_list.html'
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.all().order_by('-pk')


# NA CHWILĘ OBECNĄ POKAZUJĘ WSZYSTKIE POPULARNE Z OSTATNICH MINUT (NAJWIĘCEJ WYŚWIETLEŃ W OSTANIE 10 MIN)
# todo: ZROBIĆ NAJPOPULARNIEJSZE Z 24H, TYGODNIA, MIESIĄCA
class MostPopularArticlesListView(ListView):
    template_name = 'news/trending_articles.html'
    model = Article

    # TO QUERY POKAZUJE NAM LISTE NEWSÓW Z NAJWIĘKSZĄ ILOŚCIĄ WYŚWIETLEŃ Z OSTATNICH 10 MIN
    # MAXYMALNIE 20 NEWSÓW
    def get_queryset(self):
        period = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=10)
        return self.model.objects.filter(
            hit_count_generic__hit__created__gte=period
        ).annotate(
            counts=models.Count('hit_count_generic__hit')
        ).order_by('-counts')[:20]

# todo: DOROBIĆ INNE WIDOKI, NP TU SA WSZYSTKIE NEWSY POSORTOWANE OD NAJWIEKSZEJ ILOSCY WYSWIETLEN
# def get_queryset(self):
#     return self.model.objects.all().order_by('-hit_count_generic__hits')



class PromotedArticlesView(ListView):
    model = Article
    template_name = 'news/promoted_articles.html'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.all().order_by('-pk').filter(is_promoted=True)

class MostPopularPromotedArticlesView(ListView):
    pass

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from tinymce.models import HTMLField

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT


class Created(models.Model):
    # todo: CZY NA PEWNO null=True
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class ArticleCategory(Created):
    category_name = models.CharField(max_length=128)
    slug = models.SlugField(null=False, unique=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Article categories'


class Article(Created, HitCountMixin):
    title = models.CharField(max_length=120)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    snippet = models.TextField(null=False)  # ustawić max_lenght
    body = HTMLField(max_length=500, null=False)
    # todo: USTAWIĆ OD DELETE W CATEGORY I ZMIENIĆ RELATED NAME
    category = models.ManyToManyField(ArticleCategory, related_name='articles')
    image = models.ImageField(blank=False, null=False, upload_to='article_image/')
    is_promoted = models.BooleanField(default=False)
    slug = models.SlugField(null=False, unique=False)

    # TUTAJ TWORZĘ POWIĄZANIE OBIEKTU ABY MÓC W WIDOKACH W QUERY SORTOWAĆ PO WYŚWIETLENIACH
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def save(self, *args, **kwargs):  # opisać tą funckję
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    # METODA article_categories ZWRÓCI WSZYSTKIE KATEGORIE W STRINGU
    def article_categories(self):
        return ", \n".join([x.category_name for x in self.category.all()])

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = 'Articles'


class ArticleComment(Created):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.article.title

    class Meta:
        ordering = ['-created_on']

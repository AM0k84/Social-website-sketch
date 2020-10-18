from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from embed_video.fields import EmbedVideoField

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
from tinymce.models import HTMLField


# todo: DOROBIĆ KATEGORIĘ DO VIDEO (MANY TO MANY? CZY MOŻE JEDNAK TYLKO 1 KATEGORIĘ DLA VIDEO?)


class Base(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)  # czy na pewno null? blank?

    # todo: KLASE MOŻNA ROZSZERZYĆ O DODATKOWE FUNKCJONALNOŚCI
    class Meta:
        abstract = True


class VideoCategory(Base):
    category_name = models.CharField(max_length=128)
    slug = models.SlugField(null=False, unique=False)

    def save(self, *args, **kwargs):  # opisać tą funckję
        if not self.slug:
            self.slug = slugify(self.category_name)
        return super().save(*args, **kwargs)

    # todo: DOROBIĆ ABSOLUTE URL

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Video categories'


class Video(Base, HitCountMixin):
    video_title = models.CharField(max_length=120)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ManyToManyField(VideoCategory,
                                      related_name='cat_videos')  # todo: USTAWIĆ OD DELETE i zmienić related name
    snippet = models.TextField()
    body = HTMLField(max_length=500, null=False)
    youtube_video = EmbedVideoField(blank=False, null=False)
    is_promoted = models.BooleanField(default=False)
    slug = models.SlugField(null=False, unique=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.video_title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('video:video_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    # TUTAJ TWORZĘ POWIĄZANIE OBIEKTU ABY MÓC W WIDOKACH W QUERY SORTOWAĆ PO WYŚWIETLENIACH
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.video_title

class VideoComment(Base):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.video.video_title

    class Meta:
        ordering = ['-created_on']

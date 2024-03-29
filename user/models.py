from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from hitcount.models import HitCountMixin


class Profile(AbstractUser, HitCountMixin):
    bio = models.TextField(blank=True, null=True, default='Brak')
    slug = models.SlugField(null=False, unique=True)
    photo = models.ImageField(blank=True, null=True, upload_to='profile_photos')
    website_url = models.URLField(max_length=250, blank=True, null=True)
    instagram_url = models.URLField(max_length=250, blank=True, null=True)
    facebook_url = models.URLField(max_length=250, blank=True, null=True)
    soundcloud_url = models.URLField(max_length=250, blank=True, null=True)

    # MOŻNA UTWORZYĆ ABSOLUTE URL ABY W TEMPLAE ZAMIAST LINKU WPISYWAC ABSOLUTEURL TAK JAK W KATEGORII ARTYKULU
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Profiles'

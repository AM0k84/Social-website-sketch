import os
from audiofield.fields import AudioField
from django.conf import settings
from django.db import models


class AudioFile(models.Model):
    name = models.CharField(max_length=150, blank=False, help_text=('audio file label'))
    audio_file = AudioField(upload_to='music', blank=True,
                            ext_whitelist=('.mp3', '.wav', '.ogg'),)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    def audio_file_player(self):
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<ul class="playlist"><li style="width:250px;">\
            <a href="%s">%s</a></li></ul>' % (file_url, os.path.basename(self.audio_file.name))
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('can_view_audiofile', ('Audio File',)),
        )

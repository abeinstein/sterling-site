from django.forms import ModelForm

from apps.models import AppSettings

class AppSettingsForm(ModelForm):

    class Meta:
        model = AppSettings
        fields = ['likes_sports', 'political_bias', 'likes_books', 'likes_music', 'likes_restaurants', 'likes_games']
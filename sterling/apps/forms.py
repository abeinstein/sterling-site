from django.forms import ModelForm, Select

from apps.models import AppSettings

class AppSettingsForm(ModelForm):

    class Meta:
        model = AppSettings
        fields = ['likes_sports', 'likes_books', 'likes_music', 'likes_restaurants', 'likes_games', 'political_bias']
        widgets = {
            'political_bias': Select(choices=AppSettings.POLITICAL_CHOICES)
        }
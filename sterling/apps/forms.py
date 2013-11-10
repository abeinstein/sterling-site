from django.forms import ModelForm, Select

from apps.models import AppSettings

CITIES = (  ("NOT SET", "N/A"),
            ("ATLANTA", "ATL"),
            ("BOSTON", "BOS"),
            ("CHICAGO", "CHI"),
            ("HOUSTON", "HOU"),
            ("LOS ANGELES", "LA"),
            ("NEW YORK", "NY"),
            ("SAN FRANCISCO", "SF"),
            ("SEATTLE", "SEA"))



class AppSettingsForm(ModelForm):
    class Meta:
        model = AppSettings
        fields = ['likes_sports', 'likes_books', 'likes_music', 'likes_restaurants', 'likes_games', 'political_bias', 'city', 'social_circle']
        widgets = {
            'political_bias': Select(choices=AppSettings.POLITICAL_CHOICES),
            'city': Select(choices=CITIES),
        }
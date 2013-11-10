from django.forms import ModelForm, Select

from apps.models import AppSettings

CITIES = (  (None, "----"),
            ("Atlanta, Georgia", "ATL"),
            ("Boston, Massachusetts", "BOS"),
            ("Chicago, Illinois", "CHI"),
            ("Houston, Texas", "HOU"),
            ("Los Angeles, California", "LA"),
            ("New York, New York", "NY"),
            ("San Francisco, California", "SF"),
            ("Seattle, Washington", "SEA"))



class AppSettingsForm(ModelForm):
    class Meta:
        model = AppSettings
        fields = ['likes_sports', 'likes_books', 'likes_music', 'likes_restaurants', 'likes_games', 'political_bias', 'city', 'social_circle']
        widgets = {
            'political_bias': Select(choices=AppSettings.POLITICAL_CHOICES),
            'city': Select(choices=CITIES),
        }
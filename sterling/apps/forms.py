from django.forms import ModelForm, Select

from apps.models import AppSettings

CITIES = (  (None, "----"),
            ("Atlanta, Georgia", "Atlanta, Georgia"),
            ("Boston, Massachusetts", "Boston, Massachusetts"),
            ("Chicago, Illinois", "Chicago, Illinois"),
            ("Houston, Texas", "Houston, Texas"),
            ("Los Angeles, California", "Los Angeles, California"),
            ("New York, New York", "New York, New York"),
            ("San Francisco, California", "San Francisco, California"),
            ("Seattle, Washington", "Seattle, Washington"))

class AppSettingsForm(ModelForm):
    class Meta:
        model = AppSettings
        fields = ['likes_sports', 'likes_books', 'likes_music', 'likes_restaurants', 'likes_games', 'political_bias', 'city', 'social_circle']
        widgets = {
            'political_bias': Select(choices=AppSettings.POLITICAL_CHOICES),
            'city': Select(choices=CITIES),
        }
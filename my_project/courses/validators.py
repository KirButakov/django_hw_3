from rest_framework.exceptions import ValidationError
import re

def validate_video_url(value):
    """
    Проверяет, что ссылка на видео ведет только на youtube.com.
    """
    if not re.match(r'https?://(?:www\.)?youtube\.com/', value):
        raise ValidationError("Only YouTube links are allowed.")
    return value

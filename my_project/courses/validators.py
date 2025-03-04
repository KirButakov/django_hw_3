from rest_framework.exceptions import ValidationError
import re

def validate_video_url(value):
    """
    Проверяет, что ссылка на видео ведет только на youtube.com.
    """
    # Проверяем, что значение не пустое
    if value:
        # Используем регулярное выражение для проверки ссылок на youtube.com
        if not re.match(r'https?://(?:www\.)?(?:m\.)?youtube\.com/', value):
            raise ValidationError("Only YouTube links are allowed.")
    return value

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    year = timezone.now().year
    if year < value:
        raise ValidationError(
            'Год создания произведения указан в будущем!',
            params={'value': value},
        )

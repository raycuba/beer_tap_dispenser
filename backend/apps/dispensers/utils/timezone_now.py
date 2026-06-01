from django.utils import timezone

def timezone_now():
    """
    Devuelve la fecha y hora actual en formato timezone-aware.
    """
    return timezone.now()
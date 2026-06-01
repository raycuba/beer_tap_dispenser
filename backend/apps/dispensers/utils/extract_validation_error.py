
from django.forms import ValidationError

def extract_validation_error(e: ValidationError):
    """Extrae información útil de ValidationError"""
    if hasattr(e, 'error_dict'):
        return dict(e.error_dict)
    if hasattr(e, 'message_dict'):
        return dict(e.message_dict)
    if hasattr(e, 'messages'):
        return e.messages
    return str(e)

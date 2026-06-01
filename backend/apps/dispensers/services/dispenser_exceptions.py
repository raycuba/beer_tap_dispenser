
# services/exceptions.py

"""
EXCEPCIONES DE APLICACIÓN: 
Servicio: Orquestan la comunicación y validan el flujo de entrada.
"""

class BaseApplicationException(Exception):
    """Errores de flujo o técnicos controlados."""
    def __init__(self, *args, **kwargs):
        # Si no se pasan argumentos, usamos un mensaje por defecto
        if not args:
            args = ("Error en la operación",)
        super().__init__(*args)
        self.kwargs = kwargs

class DispenserError(BaseApplicationException):
    """Excepción base para errores relacionados con los servicios Dispenser."""
    def __init__(self, *args, **kwargs):
        if not args:
            args = ("Error en la operación de Dispenser",)
        super().__init__(*args, **kwargs)

class DispenserValidationError(DispenserError):
    """Errores de validación de datos antes de guardar el modelo."""
    def __init__(self, errors=None, *args, **kwargs):
        self.errors = errors
        msg = args[0] if args else f"Validation in Dispenser failed."
        super().__init__(msg, **kwargs)

class DispenserAlreadyExistsError(DispenserError):
    """Cuando se intenta crear una Dispenser que ya existe."""
    def __init__(self, detail=None, field="value", *args, **kwargs):
        self.field = field        
        self.detail = detail
        msg = args[0] if args else f"Dispenser already exists."
        super().__init__(msg, **kwargs)

class DispenserNotFoundError(DispenserError):
    """Cuando se intenta acceder a una Dispenser inexistente."""
    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        msg = args[0] if args else f"Dispenser with ID {id} not found."
        super().__init__(msg, **kwargs)

class DispenserOperationNotAllowedError(DispenserError):
    """Cuando se intenta realizar una operación no permitida."""
    def __init__(self, operation_name=None, *args, **kwargs):
        self.operation_name = operation_name
        msg = args[0] if args else f"Operation '{operation_name}' not allowed in Dispenser."
        super().__init__(msg, **kwargs)

class DispenserPermissionError(DispenserError):
    """Cuando el usuario no tiene permisos para modificar o acceder."""
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else "Permission not allowed in Dispenser."
        super().__init__(msg, **kwargs)

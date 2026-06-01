
# infrastructure/exceptions.py

"""
EXCEPCIONES DE REPOSITORIO:
Servicio: Abstraen los errores técnicos de la persistencia (DB, API externa).
Cuándo usarlas: Para ocultar detalles del ORM (Django) y que la App no sepa qué DB usamos.
Ejemplos: EntityNotFound, DatabaseConnectionError, UniqueConstraintViolation.

nota: no se pueden importar desde otra aplicación.
"""

class InfraestructureError(Exception):
    """Excepción base para errores técnicos (base de datos, red, etc)."""
    def __init__(self, *args, **kwargs):
        # Exception.__init__ acepta N argumentos posicionales y los guarda en .args
        super().__init__(*args)
        # Guardamos los kwargs para metadatos, trazas o lógica de respuesta
        self.kwargs = kwargs

    @property
    def message(self):
        # El primer argumento posicional suele ser el mensaje de error
        return self.args[0] if self.args else ""


# --- Errores de Lógica de Persistencia / Datos ---

class ValidationError(InfraestructureError):
    """Excepción para errores de validación de datos en la infraestructura."""
    def __init__(self, errors=None, *args, **kwargs):
        self.errors = errors
        msg = args[0] if args else "Validation failed."
        super().__init__(msg, **kwargs)


class AlreadyExistsError(InfraestructureError):
    """Excepción para cuando se intenta crear un recurso que ya existe."""
    def __init__(self, detail=None, field="value", *args, **kwargs):
        self.detail = detail
        self.field = field
        msg = args[0] if args else "Resource already exists."
        super().__init__(msg, **kwargs)


class NotFoundError(InfraestructureError):
    """Excepción para cuando no se encuentra un recurso."""
    def __init__(self, id=None, *args, **kwargs):
        self.id = id
        msg = args[0] if args else f"Resource with ID {id} not found."
        super().__init__(msg, **kwargs)


class OperationNotAllowedError(InfraestructureError):
    """Excepción para cuando se intenta realizar una operación no permitida."""
    def __init__(self, operation_name=None, *args, **kwargs):
        self.operation_name = operation_name
        msg = args[0] if args else f"Operation '{operation_name}' not allowed."
        super().__init__(msg, **kwargs)


class PermissionError(InfraestructureError):
    """Excepción para cuando el repositorio detecta falta de permisos."""
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else "Permission not allowed."
        super().__init__(msg, **kwargs)


# --- Errores Técnicos de Infraestructura ---

class RepositoryError(InfraestructureError):
    """Error genérico del repositorio (fallo al leer/escribir)."""
    pass


class ConnectionDataBaseError(InfraestructureError):
    """No se pudo conectar a la base de datos."""
    pass


class TransactionError(InfraestructureError):
    """Error al manejar una transacción."""
    pass


class SerializationError(InfraestructureError):
    """Error al serializar/deserializar datos."""
    pass

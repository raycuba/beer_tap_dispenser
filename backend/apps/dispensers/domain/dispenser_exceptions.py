
# domain/exceptions.py

"""
EXCEPCIONES DE DOMINIO:
Servicio: Protegen la integridad del modelo de negocio. 
Cuándo usarlas: Cuando una operación es técnicamente posible pero el negocio la prohíbe.
Ejemplos: InsufficientFunds, CardAlreadyExpired, PromotionLimitReached.

nota: se pueden importar desde otra aplicación
"""

from .dispenser_schemas import BaseDomainValueError

class DispenserValueError(BaseDomainValueError):
    """Error de valor en atributos de la entidad Dispenser."""
    def __init__(self, detail: str, field: str = "value", *args, **kwargs):
        self.field = field
        self.detail = detail
        if field == "value":
            super().__init__(f"Value error: {detail}.", *args, **kwargs)
        else:
            super().__init__(f"Field error in '{field}': {detail}.", *args, **kwargs)


# entity in pydantic format

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any, ClassVar
from typing_extensions import Self
from uuid import UUID
from datetime import datetime
from .dispenserusage_exceptions import *
from .dispenserusage_schemas import FileData, BaseEntity

class DispenserUsageEntity(BaseEntity):
    """
    Entidad del dominio para dispenserUsage.

    Esta clase representa la lógica de negocio central y las reglas asociadas 
    con dispenserUsage en el sistema.
    """

    domain_value_error_class: ClassVar[type] = DispenserUsageValueError    

    class Meta:
        required_fields = {"flow_volume"} # Requeridos para la creación
        readonly_fields = {"id"} # Prohibidos siempre en creacion/actualizaciones
        protected_fields = {"dispenser_id"} # Prohibidos en ciertas operaciones y actualizaciones
        special_update_fields = {"flow_volume"} # Prohibidos en actualizaciones normales, requieren manejo especial
        readonly_and_protected_fields = readonly_fields.union(protected_fields)
        special_readonly_and_protected_fields = special_update_fields.union(readonly_and_protected_fields)

    # Identificadores
    id: Optional[int] = None  # ID relacionado con la base de datos

    # Relaciones
    dispenser_id: Optional[UUID] = None  # UUID del dispensador relacionado
    
    # Atributos principales
    flow_volume: Optional[float] = None  # copia estática del flow_volume en el momento de la apertura
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    # Descomentar si se quiere hacer una validacion estricta
    #def __post_init__(self):
    #    self.validate()   

    def validate(self) -> Self:
        """
        Valida la entidad antes de guardar o procesar.

        Lanza excepciones si las reglas de negocio no se cumplen.
        - Consistencia interna de los atributos
        - Validaciones intrínsecas al momento de creación/modificación
        """
        if not self.flow_volume or self.flow_volume <= 0:
            raise self.domain_value_error_class(field="flow_volume", detail="flow_volume debe ser mayor que 0")

        return self


    def total_spent(self, now:datetime):
        """
        Calcula el dinero gastado en este uso específico.
        Precio de referencia exigido por la prueba: 12.25€ / litro.
        Soporta consultas en tiempo real incluso si el grifo sigue abierto.
        """
        PRICE_PER_LITER = 12.25
        
        # Si el grifo sigue abierto (closed_at es null), calculamos la duración hasta "ahora mismo"
        end_time = self.closed_at if self.closed_at else now
        
        # Calculamos la diferencia en segundos (el float mantiene la precisión de los milisegundos)
        duration_seconds = (end_time - self.opened_at).total_seconds()
        
        # Evitamos problemas de sincronización de reloj de milisegundos negativos
        if duration_seconds < 0:
            duration_seconds = 0
            
        # Fórmula de la prueba: segundos * litros/segundo * precio/litro
        spent = duration_seconds * self.flow_volume * PRICE_PER_LITER
        
        # Redondeamos a 5 decimales para no perder precisión en la suma total posterior
        return round(spent, 5)
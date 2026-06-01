
# entity in pydantic format

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any, ClassVar
from typing_extensions import Self
from uuid import UUID
from datetime import datetime
from .dispenser_exceptions import *
from .dispenser_schemas import FileData, BaseEntity

class DispenserEntity(BaseEntity):
    """
    Entidad del dominio para dispenser.

    Esta clase representa la lógica de negocio central y las reglas asociadas 
    con dispenser en el sistema.
    """

    domain_value_error_class = DispenserValueError    

    class Meta:
        required_fields = {"flow_volume", "status"} # Requeridos para la creación
        readonly_fields = {"id"} # Prohibidos siempre en creacion/actualizaciones
        protected_fields = {} # Prohibidos en ciertas operaciones y actualizaciones
        special_update_fields = {"usages"} # Prohibidos en actualizaciones normales, requieren manejo especial
        readonly_and_protected_fields = readonly_fields.union(protected_fields)
        
    STATUS_CHOICES = ['open', 'close',]

    # Identificadores
    id: Optional[UUID] = None  # ID relacionado con la base de datos

    # Atributos principales
    flow_volume: Optional[float] = None  # Litros por segundo que salen del grifo (ej: 0.064)
    status: Optional[str] = None  # Estado actual del grifo

    # Relaciones Many-to-Many o Reverse FK
    usages: Optional[List[int]] = None  # Lista de IDs de entidades relacionadas DispenserUsage

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

        if not self.status or not self.status in DispenserEntity.STATUS_CHOICES:
            raise self.domain_value_error_class(field="status", detail=f"el status debe estar entre: {DispenserEntity.STATUS_CHOICES}")

        if self.usages and not all(isinstance(x, int) for x in self.relations):
            raise self.domain_value_error_class(field="usages", detail="usages debe ser una lista de enteros")  

        return self

      
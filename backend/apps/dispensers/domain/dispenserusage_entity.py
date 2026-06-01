
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
        required_fields = {"dispenser_id"} # Requeridos para la creación
        readonly_fields = {"id", "opened_at"} # Prohibidos siempre en creacion/actualizaciones
        protected_fields = {"dispenser_id"} # Prohibidos en ciertas operaciones y actualizaciones
        readonly_and_protected_fields = readonly_fields.union(protected_fields)

    # Identificadores
    id: Optional[int] = None  # ID relacionado con la base de datos

    # Relaciones
    dispenser_id: Optional[int] = None  # ID del dispensador relacionado
    
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

        
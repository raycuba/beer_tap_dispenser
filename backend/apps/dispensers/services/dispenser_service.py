
from typing import List, Optional

# importa las entidades utilizadas aqui
from ..domain.dispenser_entity import DispenserEntity

# importa las excepciones utilizadas aqui
from ..domain.dispenser_exceptions import (
    DispenserValueError,
)

from .dispenser_exceptions import (
    DispenserValidationError,
    DispenserAlreadyExistsError,
    DispenserNotFoundError,
    DispenserOperationNotAllowedError,
    DispenserPermissionError
)

from ..infrastructure.exceptions import (
    ValidationError,
    AlreadyExistsError,
    NotFoundError,
    OperationNotAllowedError,
    PermissionError,
    RepositoryError, 
    ConnectionDataBaseError
)

# importa los repositorios utilizados aqui
from ..infrastructure.dispenser_repository import DispenserRepository

class DispenserService:
    """
    Servicio para manejar las operaciones CRUD relacionadas con dispenser.

    Métodos disponibles:
        - list: Lista todas las instancias de dispenser.
        - count_all: Cuenta todas las instancias de dispenser.
        - create: Crea una nueva instancia de dispenser.
        - retrieve: Recupera una instancia de dispenser por ID.
        - update: Actualiza una instancia existente de dispenser.
        - delete: Elimina una instancia de dispenser.
    """

    #Si necesitas mantener un estado de lista de entidades
    # dispenser_list = []    


    def __init__(self, repository: Optional[ DispenserRepository ] = None):
        """
        Inicializa el servicio con el repositorio correspondiente.

        params:
            repository: Repositorio que maneja la persistencia de dispenser.
        """

        self.repository = repository or DispenserRepository()


    def list(self) -> List[dict]:
        """
        Lista instancias de dispenser.

        params:
        return: 
            Lista de la entidad
        raises:
            DispenserValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si hay un error al conectar a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        entity_list = self.repository.get_all()

        return [entity.to_dict() for entity in entity_list]      


    def count_all(self) -> int:
        """
        Cuenta todas las instancias de dispenser.

        param: 
            filters: Filtros opcionales para la consulta.
        return: 
            Número total de instancias.
        raises: 
            DispenserValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.       
            RepositoryError: Si ocurre un error inesperado (interno del sistema).             
        """

        return self.repository.count_all()


    def create(self, flow_volume) -> dict:
        """
        Crea una nueva instancia de dispenser.

        params: 
            flow_volume: # Litros por segundo que salen del grifo (ej: 0.064)
        return: 
            La entidad creada.
        raises: 
            DispenserValueError: Si el valor de entrada no es válido.
            DispenserValidationError: Si los datos no son válidos.
            DispenserAlreadyExistsError: Si ya existe un registro con el mismo nombre.            
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).            
        """

        #crear la entidad
        entity = DispenserEntity.from_dict({'flow_volume': flow_volume})

        # Guardar en el repositorio
        try:
            saved_entity = self.repository.create(entity=entity)
            
        except ValidationError as e:
            raise DispenserValidationError(e.errors) from e
        except AlreadyExistsError as e:
            raise DispenserAlreadyExistsError(field=e.field, detail=e.detail) from e

        return saved_entity.to_dict()


    def retrieve(self, entity_id: str = None) -> dict:
        """
        Recupera una instancia de dispenser por su ID o UUID.

        param: 
            entity_id: ID de la instancia a recuperar.
        return: 
            La entidad recuperada.
        raises:
            DispenserValueError: Si el valor de entrada no es válido.         
            DispenserNotFoundError: Si no existe el registro con el ID dado.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        try:
            entity = self.repository.get_by_id(id=entity_id)  
        except NotFoundError as e:
            raise DispenserNotFoundError(id=entity_id) from e

        return entity.to_dict()


    def update(self, entity_id: str = None, status = None) -> dict:
        """
        Actualiza una instancia existente de dispenser.

        params:
            entity_id: ID de la instancia a actualizar.
            status: Estado actual del grifo
        return: 
            La entidad actualizada.
        raises: 
            DispenserValueError: Si el valor de entrada no es válido.                 
            DispenserValidationError: Si los datos no son válidos.   
            DispenserNotFoundError: Si no existe el registro con el ID dado.         
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        # Validación de entrada
        if not entity_id:
            raise DispenserValueError(field="id", detail="The id or uuid field is required")
        
        if not status:
            raise DispenserValueError(field="status", detail="The status field is required")
        
        if not status in DispenserEntity.STATUS_CHOICES:
            raise DispenserValueError(field="status", detail=f"The status field must be in {DispenserEntity.STATUS_CHOICES}")

        # Recuperar la entidad
        try:
            entity = self.repository.get_by_id(id=entity_id)
        except NotFoundError as e:
            raise DispenserNotFoundError(id=entity_id) from e

        # actualizar la instancia
        entity.update({'status': status})     

        # Guardar en el repositorio
        try:
            updated_entity = self.repository.update(entity=entity)
        except NotFoundError as e:
            raise DispenserNotFoundError(id=entity_id) from e
        except ValidationError as e:
            raise DispenserValidationError(e.errors) from e

        return updated_entity.to_dict()


    def delete(self, entity_id: str = None) -> bool:
        """
        Elimina una instancia de dispenser.

        params:
            entity_id: ID de la instancia a eliminar.
            entity_uuid: UUID de la instancia a eliminar.
        return: 
            True/False (depende del exito de la operacion)
        raises:
            DispenserNotFoundError: Si no se encuentra la instancia.
            DispenserValueError: Si el valor de entrada no es válido.
            DispenserValidationError: Si los datos no son válidos.            
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).            
        """
        # Validación de entrada
        if not entity_id:
            raise DispenserValueError(field="id", detail="The id field is required")

        # Eliminación en el repositorio
        try:
            self.repository.delete(id=entity_id)
        except NotFoundError as e:
            raise DispenserNotFoundError(id=entity_id) from e
        except ValidationError as e:
            raise DispenserValidationError(e.errors) from e

        return True

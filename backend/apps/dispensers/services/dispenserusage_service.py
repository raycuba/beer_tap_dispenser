
from typing import List, Optional

# importa las entidades utilizadas aqui
from ..domain.dispenserusage_entity import DispenserUsageEntity

# importa las excepciones utilizadas aqui
from ..domain.dispenserusage_exceptions import (
    DispenserUsageValueError,
)

from .dispenserusage_exceptions import (
    DispenserUsageValidationError,
    DispenserUsageAlreadyExistsError,
    DispenserUsageNotFoundError,
    DispenserUsageOperationNotAllowedError,
    DispenserUsagePermissionError
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
from ..infrastructure.dispenserusage_repository import DispenserUsageRepository

class DispenserUsageService:
    """
    Servicio para manejar las operaciones CRUD relacionadas con dispenserUsage.

    Métodos disponibles:
        - list: Lista todas las instancias de dispenserUsage.
        - count_all: Cuenta todas las instancias de dispenserUsage.
        - create: Crea una nueva instancia de dispenserUsage.
        - retrieve: Recupera una instancia de dispenserUsage por ID.
        - update: Actualiza una instancia existente de dispenserUsage.
        - delete: Elimina una instancia de dispenserUsage.
    """

    #Si necesitas mantener un estado de lista de entidades
    # dispenserUsage_list = []    


    def __init__(self, repository: Optional[ DispenserUsageRepository ] = None):
        """
        Inicializa el servicio con el repositorio correspondiente.

        params:
            repository: Repositorio que maneja la persistencia de dispenserUsage.
        """

        self.repository = repository or DispenserUsageRepository()


    def list(self, filters: Optional[dict] = None) -> List[dict]:
        """
        Lista instancias de dispenserUsage.

        params:
            filters: Filtros opcionales para la consulta.
        return: 
            Lista de la entidad
        raises:
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si hay un error al conectar a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        entity_list = self.repository.get_all(filters=filters)

        return [entity.to_dict() for entity in entity_list]      


    def count_all(self, filters: Optional[dict] = None) -> int:
        """
        Cuenta todas las instancias de dispenserUsage.

        param: 
            filters: Filtros opcionales para la consulta.
        return: 
            Número total de instancias.
        raises: 
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.       
            RepositoryError: Si ocurre un error inesperado (interno del sistema).             
        """

        return self.repository.count_all(filters=filters)


    def create(self, data, dispenser_id: Optional[str]=None) -> dict:
        """
        Crea una nueva instancia de dispenserUsage.

        params: 
            data: Diccionario o DTO con los datos necesarios para crear la instancia.
            dispenser_id: ID del padre si es necesario (opcional).
        return: 
            La entidad creada.
        raises: 
            DispenserUsageValueError: Si el valor de entrada no es válido.
            DispenserUsageValidationError: Si los datos no son válidos.
            DispenserUsageAlreadyExistsError: Si ya existe un registro con el mismo nombre.            
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).            
        """

        #crear la entidad
        entity = DispenserUsageEntity.from_dict(data)  

        # Guardar en el repositorio
        try:
            saved_entity = self.repository.create(entity=entity, dispenser_id=dispenser_id)
        except ValidationError as e:
            raise DispenserUsageValidationError(e.errors) from e
        except AlreadyExistsError as e:
            raise DispenserUsageAlreadyExistsError(field=e.field, detail=e.detail) from e

        return saved_entity.to_dict()


    def retrieve(self, entity_id: int = None) -> dict:
        """
        Recupera una instancia de dispenserUsage por su ID o UUID.

        param: 
            entity_id: ID de la instancia a recuperar.
        return: 
            La entidad recuperada.
        raises:
            DispenserUsageValueError: Si el valor de entrada no es válido.         
            DispenserUsageNotFoundError: Si no existe el registro con el ID dado.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        try:
            entity = self.repository.get_by_id(id=entity_id)  
        except NotFoundError as e:
            raise DispenserUsageNotFoundError(id=entity_id) from e

        return entity.to_dict()


    def update(self, entity_id: int = None, data = None) -> dict:
        """
        Actualiza una instancia existente de dispenserUsage.

        params:
            entity_id: ID de la instancia a actualizar.
            data: Diccionario o DTO con los datos a actualizar.
        return: 
            La entidad actualizada.
        raises: 
            DispenserUsageValueError: Si el valor de entrada no es válido.                 
            DispenserUsageValidationError: Si los datos no son válidos.   
            DispenserUsageNotFoundError: Si no existe el registro con el ID dado.         
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        
        # Validación de entrada
        if not entity_id:
            raise DispenserUsageValueError(field="id", detail="The id or uuid field is required")
        
        if not data:
            raise DispenserUsageValueError(field="data", detail="The data field is required")

        # Recuperar la entidad
        try:
            entity = self.repository.get_by_id(id=entity_id)
        except NotFoundError as e:
            raise DispenserUsageNotFoundError(id=entity_id) from e

        # actualizar la instancia
        entity.update(data)     
        print(f"DispenserUsageService.Entity updated: {entity}")

        # Guardar en el repositorio
        try:
            updated_entity = self.repository.update(entity=entity)
        except NotFoundError as e:
            raise DispenserUsageNotFoundError(id=entity_id) from e
        except ValidationError as e:
            raise DispenserUsageValidationError(e.errors) from e

        return updated_entity.to_dict()


    def delete(self, entity_id: int = None) -> bool:
        """
        Elimina una instancia de dispenserUsage.

        params:
            entity_id: ID de la instancia a eliminar.
        return: 
            True/False (depende del exito de la operacion)
        raises:
            DispenserUsageNotFoundError: Si no se encuentra la instancia.
            DispenserUsageValueError: Si el valor de entrada no es válido.
            DispenserUsageValidationError: Si los datos no son válidos.            
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).            
        """
        # Validación de entrada
        if not entity_id:
            raise DispenserUsageValueError(field="id", detail="The id field is required")

        # Eliminación en el repositorio
        try:
            self.repository.delete(id=entity_id)
        except NotFoundError as e:
            raise DispenserUsageNotFoundError(id=entity_id) from e
        except ValidationError as e:
            raise DispenserUsageValidationError(e.errors) from e

        return True


from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import Q
from django.forms import ValidationError as DjangoValidationError

# importa las entidades utilizadas aqui
from ..models import Dispenser
from .mappers import Mapper
from ..utils.filter_dict import clean_dict_of_keys
from ..utils.is_integer import is_integer
from ..utils.is_uuid import is_uuid
from ..utils.extract_validation_error import extract_validation_error
from ..domain.dispenser_entity import DispenserEntity


# importa las excepciones personalizadas
from ..domain.dispenser_exceptions import (
    DispenserValueError,
)

from .exceptions import (
    ValidationError,
    AlreadyExistsError,
    NotFoundError,
    OperationNotAllowedError,
    PermissionError,
    ConnectionDataBaseError,
    RepositoryError
)


class DispenserRepository:
    """
    Repositorio para manejar la persistencia de datos de la entidad: dispenser.
    
    Este repositorio incluye:
    - Validación de existencia de registros.
    - Control de unicidad.
    - Métodos básicos.
    """

    @staticmethod
    def get_all() -> List[ DispenserEntity ]:
        """
        Obtiene todos los registros de la entidad.

        params:
        returns: 
            List[ DispenserEntity ]: Lista de entidades recuperadas.
        raises:
            DispenserValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si hay un error al conectar a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """

        try:
            instance_list = Dispenser.objects.all()    

            # Convertir a entidades usando el Mapper genérico
            return [Mapper.model_to_entity(instance, DispenserEntity) for instance in instance_list]        

        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e
        except Exception as e:
            raise RepositoryError(f"Error fetching registers: {str(e)}") from e


    @staticmethod
    def get_by_id(id = None) -> Optional[ DispenserEntity ]:
        """
        Obtiene un registro por su ID o UUID.
        
        params:
            id: ID del registro a recuperar.
        returns: 
            El entidad encontrada o None si no existe.
        raises:
            DispenserValueError: Si el valor de entrada no es válido.        
            NotFoundError: Si no existe el registro con el ID dado.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """

        # Validar que el ID sea un entero o el UUID sea un UUID válido
        if id is None or not is_uuid(id):
                raise DispenserValueError(field="id", detail="ID must be UUID.")

        try:
            instance = Dispenser.objects.get(id=id)

            return Mapper.model_to_entity(instance, DispenserEntity)

        except Dispenser.DoesNotExist as e:
            raise NotFoundError(id=id) from e
        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e    
        except Exception as e:
            raise RepositoryError(f"Error fetching registers with ID {id}: {str(e)}") from e            
     

    @staticmethod
    def exists_by_field(field_name, value) -> bool:
        """
        Verifica si existe un registro con un valor específico para un campo dado.

        params: 
            field_name: Nombre del campo a buscar.
            value: Valor del campo a verificar.
        returns:
            True si existe un registro con el valor dado, False en caso contrario.
        raises:
            DispenserValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """
        
        # Lista de campos en los que se permite verificar existencia
        ALLOWED_FIELDS = ['status']  # define según tu entidad
        
        if field_name not in ALLOWED_FIELDS:
            raise DispenserValueError(field=field_name, detail=f"El campo '{field_name}' no es válido para verificar existencia.")

        try:
            return Dispenser.objects.filter(**{field_name: value}).exists()

        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e
        except Exception as e:
            raise RepositoryError(f"Error verifying field {field_name} with value {value}: {str(e)}") from e            


    @staticmethod
    def count_all() -> int:
        """
        Cuenta registros que cumplen con ciertas condiciones.

        params: 
            filters: Condiciones de filtro como clave-valor.
        returns:
            Número de registros que cumplen las condiciones.
        raises: 
            DispenserValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.       
            RepositoryError: Si ocurre un error inesperado (interno del sistema). 
        """     

        try:
            instance_list = Dispenser.objects.all()      

            return instance_list.count()            

        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e            
        except Exception as e:
            raise RepositoryError(f"Error counting registers: {str(e)}") from e


    @staticmethod
    def create(entity: DispenserEntity) -> DispenserEntity:
        """
        Crea un nuevo registro.

        params: 
            entity: Entidad con los datos necesarios para crear el registro.
        returns: 
            La entidad creada.
        raises:
            DispenserValueError:  Si el valor de entrada no es válido.
            ValidationError: Si los datos no son válidos.
            AlreadyExistsError: Si ya existe un registro con el mismo nombre.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.   
            RepositoryError: Si ocurre un error inesperado (interno del sistema).     
        """

        # Validar la entidad de entrada
        if not entity or not hasattr(entity, "to_dict"):
            raise DispenserValueError(field="Dispenser", detail="Entity null or without methond 'to_dict'")

        try:
            # Crear el registro a partir de los campos presentes en la 'entity'
            instance = Dispenser()

            with transaction.atomic():
                # Asegurar que todas las operaciones se realicen en una transacción
                # Esto garantiza que si algo falla, no se guarden cambios parciales    
                
                # Actualizar cada campo de la entidad en el modelo
                Mapper.update_model_from_entity(instance, entity, excluded_fields=DispenserEntity.Meta.special_readonly_and_protected_fields)      

                # Validar y guardar
                instance.full_clean()  # Validaciones del modelo
                instance.save()            

        except (TypeError, ValueError) as e:
            raise DispenserValueError(field="data", detail=f"Error in the data structure: {str(e)}") from e
        except DjangoValidationError as e:
            error_detail = extract_validation_error(e)
            raise ValidationError(f"Validation error: {error_detail}") from e
        except IntegrityError as e:
            if 'duplicate' in str(e).lower() or 'unique constraint' in str(e).lower():
                raise AlreadyExistsError(field='name', detail=instance.name)  # Ajusta según el campo único
            # Otro error de integridad → regla de negocio?
            raise ValidationError({"integrity": "Duplicated or inconsistent data"})            
        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e
        except Exception as e:
            raise RepositoryError(f"Error creating register: {str(e)}") from e
        
        return Mapper.model_to_entity(instance, DispenserEntity)


    @staticmethod
    def update(entity: DispenserEntity) -> DispenserEntity:
        """
        Guarda los cambios en una entidad existente.

        params: 
            entity: Entidad con los datos a actualizar (debe traer el id en los campos).
        returns:
            La entidad guardada.
        raises: 
            DispenserValueError:  Si el valor de entrada no es válido.
            NotFoundError: Si no existe el registro con el ID dado.
            ValidationError: Si los datos no son válidos.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.   
            RepositoryError: Si ocurre un error inesperado (interno del sistema).     
        """    

        # Validar la entidad de entrada
        if not entity or not hasattr(entity, "to_dict"):
            raise DispenserValueError(field="Dispenser", detail="Entity null or without method 'to_dict'")

        # validar el id
        if not entity.id or not is_uuid(entity.id):
            raise DispenserValueError(field="id", detail="Id must be UUID.")

        try:
            instance = Dispenser.objects.get(id=entity.id)

            with transaction.atomic():
                # Asegurar que todas las operaciones se realicen en una transacción
                # Esto garantiza que si algo falla, no se guarden cambios parciales     
                
                # Actualizar cada campo de la entidad en el modelo
                Mapper.update_model_from_entity(instance, entity, excluded_fields=DispenserEntity.Meta.readonly_and_special_fields)           

                instance.full_clean()  # Validaciones del modelo Django
                instance.save()       
            
            # Convertir el modelo actualizado de vuelta a una entidad
            return Mapper.model_to_entity(instance, DispenserEntity)

        except Dispenser.DoesNotExist as e:
            raise NotFoundError(id=entity.id) from e
        except (TypeError, ValueError) as e:
            raise DispenserValueError(field="data", detail=f"Error in the data structure: {str(e)}") from e
        except DjangoValidationError as e:
            error_detail = extract_validation_error(e)
            raise ValidationError(f"Validation error: {error_detail}") from e
        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e            
        except Exception as e:
            raise RepositoryError(f"Error updating register: {str(e)}") from e


    @staticmethod
    def delete(id=None) -> bool:
        """
        Elimina un registro por su ID o UUID.

        params: 
            id: ID del registro a eliminar.
        raises: 
            DispenserValueError:  Si el valor de entrada no es válido.
            NotFoundError: Si no existe el registro con el ID dado.
            ValidationError: Si los datos no son válidos
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.      
            RepositoryError: Si ocurre un error inesperado (interno del sistema).  
        returns: 
            True si la eliminación fue exitosa
        """

        # validar el id
        if id is not None and not is_uuid(id):
            raise DispenserValueError(field="id", detail="El ID debe ser un UUID.")

        try:
            instance = Dispenser.objects.get(id=id)
    
            instance.delete()
            return True

        except Dispenser.DoesNotExist as e:
            raise NotFoundError(id=id) from e
        except DjangoValidationError as e:
            error_detail = extract_validation_error(e)
            raise ValidationError(f"Validation error occurred: {error_detail}") from e
        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e            
        except Exception as e:
            raise RepositoryError(f"Error deleting register: {str(e)}") from e


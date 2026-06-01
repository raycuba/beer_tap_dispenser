
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import Q
from django.forms import ValidationError as DjangoValidationError

# importa las entidades utilizadas aqui
from ..models import DispenserUsage
from .mappers import Mapper
from ..utils.filter_dict import clean_dict_of_keys
from ..utils.is_integer import is_integer
from ..utils.is_uuid import is_uuid
from ..utils.extract_validation_error import extract_validation_error
from ..domain.dispenserusage_entity import DispenserUsageEntity


# importa las excepciones personalizadas
from ..domain.dispenserusage_exceptions import (
    DispenserUsageValueError,
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


class DispenserUsageRepository:
    """
    Repositorio para manejar la persistencia de datos de la entidad: dispenserUsage.
    
    Este repositorio incluye:
    - Validación de existencia de registros.
    - Control de unicidad.
    - Métodos básicos.
    """

    @staticmethod
    def get_all(filters: Optional[dict] = None) -> List[ DispenserUsageEntity ]:
        """
        Obtiene todos los registros de la entidad.

        params:
            filters (dict, optional): Filtros a aplicar en la consulta.
        returns: 
            List[ DispenserUsageEntity ]: Lista de entidades recuperadas.
        raises:
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si hay un error al conectar a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """

        try:
            instance_list = DispenserUsage.objects.all()    

            # Aplicar filtros si se proporcionan
            if filters is not None:
                if not isinstance(filters, dict):
                    raise DispenserUsageValueError(field="filters", detail="filters must be dict or None")
                if "dispenser_id" in filters and filters["dispenser_id"]:
                    instance_list = instance_list.filter(dispenser_id=filters["dispenser_id"])      
                if "closed_at" in filters:
                    if filters["closed_at"] == 'null' or filters["closed_at"] == 'None' or filters["closed_at"] == '':
                        instance_list = instance_list.filter(closed_at__isnull=True)
                    else:
                        instance_list = instance_list.filter(closed_at=filters["closed_at"])

            # Convertir a entidades usando el Mapper genérico
            return [Mapper.model_to_entity(instance, DispenserUsageEntity) for instance in instance_list]        

        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e
        except Exception as e:
            raise RepositoryError(f"Error fetching registers: {str(e)}") from e


    @staticmethod
    def get_by_id(id = None) -> Optional[ DispenserUsageEntity ]:
        """
        Obtiene un registro por su ID.
        
        params:
            id: ID del registro a recuperar.
        returns: 
            El entidad encontrada o None si no existe.
        raises:
            DispenserUsageValueError: Si el valor de entrada no es válido.        
            NotFoundError: Si no existe el registro con el ID dado.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.
            RepositoryError: Si ocurre un error inesperado (interno del sistema).
        """

        # Validar que el ID sea un entero o el UUID sea un UUID válido
        if id is None or not is_integer(id):
                raise DispenserUsageValueError(field="id", detail="ID must be integer.")

        try:
            instance = DispenserUsage.objects.get(id=id)

            return Mapper.model_to_entity(instance, DispenserUsageEntity)

        except DispenserUsage.DoesNotExist as e:
            raise NotFoundError(id=id) from e
        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e    
        except Exception as e:
            raise RepositoryError(f"Error fetching registers with ID {id}: {str(e)}") from e            
              


    @staticmethod
    def count_all(filters: Optional[dict] = None) -> int:
        """
        Cuenta registros que cumplen con ciertas condiciones.

        params: 
            filters: Condiciones de filtro como clave-valor.
        returns:
            Número de registros que cumplen las condiciones.
        raises: 
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.       
            RepositoryError: Si ocurre un error inesperado (interno del sistema). 
        """     

        try:
            instance_list = DispenserUsage.objects.all()    

            # Aplicar filtros si se proporcionan
            if filters is not None:
                if not isinstance(filters, dict):
                    raise DispenserUsageValueError(field="filters", detail="filters must be dict or None")
                if "dispenser_id" in filters and filters["dispenser_id"].strip():
                    instance_list = instance_list.filter(dispenser_id=filters["dispenser_id"])      
                if "closed_at" in filters and filters["closed_at"].strip():
                    instance_list = instance_list.filter(closed_at=filters["closed_at"])        

            return instance_list.count()            

        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e            
        except Exception as e:
            raise RepositoryError(f"Error counting registers: {str(e)}") from e


    @staticmethod
    def create(entity: DispenserUsageEntity, dispenser_id: Optional[str]) -> DispenserUsageEntity:
        """
        Crea un nuevo registro.

        params: 
            entity: Entidad con los datos necesarios para crear el registro.
            dispenser_id: ID del padre si es necesario (opcional).
        returns: 
            La entidad creada.
        raises:
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            ValidationError: Si los datos no son válidos.
            AlreadyExistsError: Si ya existe un registro con el mismo nombre.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.   
            RepositoryError: Si ocurre un error inesperado (interno del sistema).     
        """

        # Validar la entidad de entrada
        if not entity or not hasattr(entity, "to_dict"):
            raise DispenserUsageValueError(field="DispenserUsage", detail="Entity null or without methond 'to_dict'")

        try:
            # Crear el registro a partir de los campos presentes en la 'entity'
            instance = DispenserUsage()

            with transaction.atomic():
                # Asegurar que todas las operaciones se realicen en una transacción
                # Esto garantiza que si algo falla, no se guarden cambios parciales    
                
                # Actualizar cada campo de la entidad en el modelo
                Mapper.update_model_from_entity(instance, entity, excluded_fields=DispenserUsageEntity.Meta.readonly_and_protected_fields)            

                # Si se proporciona un ID de otra entidad, actualizarlo
                # django crea el campo 'dispenser_id' automáticamente si la relación es ForeignKey => otherEntity
                if dispenser_id is not None:
                    instance.dispenser_id = dispenser_id

                # Validar y guardar
                instance.full_clean()  # Validaciones del modelo
                instance.save()              

        except (TypeError, ValueError) as e:
            raise DispenserUsageValueError(field="data", detail=f"Error in the data structure: {str(e)}") from e
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
        
        return Mapper.model_to_entity(instance, DispenserUsageEntity)


    @staticmethod
    def update(entity: DispenserUsageEntity) -> DispenserUsageEntity:
        """
        Guarda los cambios en una entidad existente.

        params: 
            entity: Entidad con los datos a actualizar (debe traer el id en los campos).
        returns:
            La entidad guardada.
        raises: 
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            NotFoundError: Si no existe el registro con el ID dado.
            ValidationError: Si los datos no son válidos.
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.   
            RepositoryError: Si ocurre un error inesperado (interno del sistema).     
        """    

        # Validar la entidad de entrada
        if not entity or not hasattr(entity, "to_dict"):
            raise DispenserUsageValueError(field="DispenserUsage", detail="Entity null or without method 'to_dict'")

        # validar el id
        if not entity.id or not is_integer(entity.id):
            raise DispenserUsageValueError(field="id", detail="Id must be integer.")

        try:
            instance = DispenserUsage.objects.get(id=entity.id)

            with transaction.atomic():
                # Asegurar que todas las operaciones se realicen en una transacción
                # Esto garantiza que si algo falla, no se guarden cambios parciales     
        
                # Actualizar cada campo de la entidad en el modelo
                Mapper.update_model_from_entity(instance, entity, excluded_fields=DispenserUsageEntity.Meta.special_readonly_and_protected_fields)   

                instance.full_clean()  # Validaciones del modelo Django
                instance.save()            
            
            # Convertir el modelo actualizado de vuelta a una entidad
            return Mapper.model_to_entity(instance, DispenserUsageEntity)

        except DispenserUsage.DoesNotExist as e:
            raise NotFoundError(id=entity.id) from e
        except (TypeError, ValueError) as e:
            raise DispenserUsageValueError(field="data", detail=f"Error in the data structure: {str(e)}") from e
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
        Elimina un registro por su ID.

        params: 
            id: ID del registro a eliminar.
        raises: 
            DispenserUsageValueError:  Si el valor de entrada no es válido.
            NotFoundError: Si no existe el registro con el ID dado.
            ValidationError: Si los datos no son válidos
            ConnectionDataBaseError: Si ocurre un error al acceder a la base de datos.      
            RepositoryError: Si ocurre un error inesperado (interno del sistema).  
        returns: 
            True si la eliminación fue exitosa
        """

        # validar el id
        if id is not None and not is_integer(id):
            raise DispenserUsageValueError(field="id", detail="El ID debe ser un entero.")


        try:
            instance = DispenserUsage.objects.get(id=id)
    
            instance.delete()
            return True

        except DispenserUsage.DoesNotExist as e:
            raise NotFoundError(id=id) from e
        except DjangoValidationError as e:
            error_detail = extract_validation_error(e)
            raise ValidationError(f"Validation error occurred: {error_detail}") from e
        except DatabaseError as e:
            raise ConnectionDataBaseError("Data base access error") from e            
        except Exception as e:
            raise RepositoryError(f"Error deleting register: {str(e)}") from e


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from apps.dispensers.utils.is_valid_utc_z import is_valid_utc_z

# importar serializers
from .serializers.dispenser_serializer import (
    DispenserDTOSerializer,
    CreateDispenserSerializer,
    CreateDispenserResultSerializer,
    ChangeDispenserSerializer
)

# importa las excepciones personalizadas
from .domain.dispenser_exceptions import (
    DispenserValueError,
)
from .domain.dispenserusage_exceptions import (
    DispenserUsageValueError,
)

from .services.dispenser_exceptions import (
    DispenserValidationError,
    DispenserAlreadyExistsError,
    DispenserNotFoundError,
    DispenserOperationNotAllowedError,
    DispenserPermissionError
)

# importa las excepciones de repositorio
from .infrastructure.exceptions import (
    ConnectionDataBaseError,
    RepositoryError
)

# importar servicios específicos del dominio
from apps.dispensers.services.dispenser_service import DispenserService

"""
Códigos de estado HTTP a utilizar en las respuestas:
- 200 OK: La solicitud se ha procesado correctamente y se devuelve la información solicitada.
- 201 Created: La solicitud se ha procesado correctamente y se ha creado un nuevo recurso (no aplicable en estos endpoints, pero útil para futuras expansiones).
- 204 No Content: La solicitud se ha procesado correctamente pero no hay contenido que devolver (no aplicable en estos endpoints, pero útil para futuras expansiones).
- 400 Bad Request: La solicitud no se ha podido procesar debido a errores de validación o datos incorrectos. Se devuelve un mensaje de error detallado en el cuerpo de la respuesta.
- 401 Unauthorized: El usuario no está autenticado. Se requiere autenticación para acceder a este recurso.
- 403 Forbidden: El usuario está autenticado pero no tiene permisos para acceder a este recurso.
- 404 Not Found: El recurso solicitado no se ha encontrado, como un client card o una promoción específica.
- 409 Conflict: Se ha producido un conflicto al intentar procesar la solicitud, como intentar reclamar una tarjeta que ya ha sido reclamada.
- 500 Internal Server Error: Se ha producido un error inesperado en el servidor al procesar la solicitud. Se devuelve un mensaje de error genérico.
"""

class DispenserViewSet(ViewSet):
    """
    ViewSet para manejar operaciones CRUD relacionadas con dispenser.
    
    Este ViewSet interactúa con:
    - Los servicios del dominio para manejar la lógica de negocio.
    - Los repositorios para acceder a la capa de persistencia.
    """

    # Serializer por defecto para documentación
    serializer_class = DispenserDTOSerializer    

    # Definición de permisos y autenticación
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    # Definición de métodos HTTP permitidos
    # http_method_names = ['get', 'post', 'put', 'delete']


    @extend_schema(
        operation_id="dispenser_list",
        summary="Retrieve a list or a specific dispenser",
        description="Retrieve a list of all dispenser or a specific one by ID",
        responses={
            200: DispenserDTOSerializer(many=True),
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["dispensers"]
    )
    def list(self, request):
        """
        Endpoint para obtener una lista de todos los dispenser.
        
        - Se valida y adapta la solicitud.
        - Se utiliza el servicio `list_dispenser` para manejar la lógica.
        """

        dispenserService = DispenserService() # Instanciar el servicio

        try:
            # Llamar al servicio para recuperar todos los registros
            dispenserList = dispenserService.list()

            # Serializar la lista de registros
            response_serializer_list = DispenserDTOSerializer(dispenserList, many=True)       

            # Retornar los datos serializados con un estado HTTP 200 OK
            return Response(response_serializer_list.data, status=status.HTTP_200_OK)

        except (DispenserValueError) as e:
            # Manejar errores de validación si los datos no son válidos
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="dispenser_retrieve",
        summary="Retrieve a specific dispenser by ID",
        description="Retrieve a specific dispenser by its ID",
        responses={
            200: DispenserDTOSerializer,
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["dispensers"]
    )
    def retrieve(self, request, pk: str = None):
        """
        Endpoint para obtener un dispenser específico por su ID (pk).
        
        - Valida y adapta la solicitud al dominio.
        - Utiliza el servicio `retrieve_dispenser` para manejar la lógica.
        """

        dispenserService = DispenserService() # Instanciar el servicio

        try:
            # Llamar al servicio para recuperar un registro específico
            dispenser = dispenserService.retrieve(entity_id=pk)

            # Serializar el registro recuperado
            response_serializer = DispenserDTOSerializer(dispenser)        

            # Retornar el resultado con un estado HTTP 200 OK
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except DispenserNotFoundError as e:
            # Manejar errores si no se encuentra el registro
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except DispenserValueError as e:
            # Manejar errores de validación si el ID no es válido
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="dispenser_create",
        summary="Create a new dispenser",
        description="Create a new dispenser with the provided data",
        request=CreateDispenserSerializer,
        responses={
            201: CreateDispenserResultSerializer,
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["dispensers"]
    )
    def create(self, request):
        """
        Endpoint para crear un nuevo dispenser.
        
        - Valida y adapta los datos entrantes.
        - Llama al servicio `create_dispenser` para manejar la creación.
        """
        
        # Datos enviados en el cuerpo de la solicitud
        serializer = CreateDispenserSerializer(data=request.data)
        if not serializer.is_valid():
            # Si la validación falla, retornar un error 400 BAD REQUEST
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # Obtener el flow_volume
        flow_volume = data.get('flow_volume', None)
        if flow_volume is None or flow_volume <= 0:
            return Response({"error": "flow_volume is required and must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
        
        dispenserService = DispenserService() # Instanciar el servicio

        try:
            # Llamar al servicio para crear el registro
            dispenser = dispenserService.create(flow_volume=flow_volume)

            # Serializar el nuevo registro creado
            response_serializer = DispenserDTOSerializer(dispenser)      

            # Retornar el resultado con un estado HTTP 201 CREATED
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except DispenserAlreadyExistsError as e:
            # Manejar errores si ya existe un registro con el mismo nombre
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (DispenserValueError, DispenserValidationError) as e:
            # Manejar errores de validación si los datos no son válidos
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="dispenser_update",
        summary="Update an existing dispenser",
        description="Update an existing dispenser with the provided ID and data",
        request=ChangeDispenserSerializer,
        responses={
            200: OpenApiResponse(description="OK"),
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found")
        },
        tags=["dispensers"]
    )
    def update(self, request, pk: str = None):
        """
        Endpoint para actualizar un dispenser existente.
        
        - Valida y adapta los datos entrantes.
        - Llama al servicio `update_dispenser` para manejar la actualización.
        """
        print(f"DispenserViewSet: Received update request for dispenser with id {pk} with data: {request.data}")

        # Datos enviados en el cuerpo de la solicitud
        serializer = ChangeDispenserSerializer(data=request.data) 
        if not serializer.is_valid():
            # Si la validación falla, retornar un error 400 BAD REQUEST
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # Obtener el status
        status_q = data.get('status', None)
        updated_at_q = data.get('updated_at', None)
        print(f"DispenserViewSet: Validated data for update - status: {status_q}, updated_at: {updated_at_q}")
        
        # Validar que el status sea 'open' o 'close' y que updated_at esté presente y sea una fecha válida
        if status_q is None or not status_q in ['open', 'close']:
            return Response({"error": "status is required and must be either 'open' or 'close'"}, status=status.HTTP_400_BAD_REQUEST)
        if updated_at_q is None:
            return Response({"error": "updated_at is required and must be a valid utc date string"}, status=status.HTTP_400_BAD_REQUEST)
                         
        dispenserService = DispenserService() # Instanciar el servicio

        try:
            # Llamar al servicio para actualizar el registro
            print(f"DispenserViewSet: Attempting to update dispenser with id {pk} to status '{status_q}' at {updated_at_q}")
            dispenser = dispenserService.update(entity_id=pk, status=status_q, updated_at=updated_at_q)
            print(f"DispenserViewSet: Successfully updated dispenser with id {pk} dispenser: {dispenser}")

            # Serializar el registro actualizado
            response_serializer = DispenserDTOSerializer(dispenser)          

            # Retornar el resultado con un estado HTTP 200 OK
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        except DispenserNotFoundError as e:
            # Manejar errores si no se encuentra el registro con el ID dado
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (DispenserValueError, DispenserValidationError) as e:
            # Manejar errores de validación si los datos no son válidos
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @extend_schema(
        operation_id="dispenser_delete",
        summary="Delete an existing dispenser",
        description="Delete an existing dispenser with the provided ID",
        responses={
            204: OpenApiResponse(description="No Content"),
            400: OpenApiResponse(description="Bad Request"),
            404: OpenApiResponse(description="Not Found")
        },
        tags=["dispensers"]
    )
    def destroy(self, request, pk: str = None):
        """
        Endpoint para eliminar un dispenser existente.
        
        - Valida y adapta la solicitud.
        - Llama al servicio `delete_dispenser` para manejar la eliminación.
        """

        dispenserService = DispenserService() # Instanciar el servicio

        try:
            # Llamar al servicio para eliminar el registro
            dispenser = dispenserService.delete(entity_id=pk)

            # Retornar un estado HTTP 204 NO CONTENT para confirmar la eliminación
            return Response(status=status.HTTP_204_NO_CONTENT)

        except DispenserNotFoundError as e:
            # Manejar errores si no se encuentra el registro con el ID dado
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (DispenserValueError, DispenserValidationError) as e:
            # Manejar errores de validación si el ID no es válido
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            # Manejar errores de conexión a la base de datos o repositorio
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    @extend_schema(
        operation_id="dispenser_get_total_spent_by_dispenser",
        summary="Get total spent by dispenser",
        description="Get the total amount spent by a specific dispenser by its ID",
        responses={
            200: OpenApiResponse(description="OK"),
            404: OpenApiResponse(description="Not Found"),
            400: OpenApiResponse(description="Bad Request")
        },
        tags=["dispensers"]
    )
    def get_total_spent_by_dispenser(self, request, pk: str = None):
        """
        Endpoint para obtener el total gastado por un dispenser específico.
        """
        dispenserService = DispenserService()

        try:
            total_spent_dto = dispenserService.get_total_spent_by_dispenser(dispenser_id=pk)
            return Response(
                {"dispenser_id": pk, "total_spent": total_spent_dto.amount, "usages": [usage.to_dict() for usage in total_spent_dto.usages]},
                status=status.HTTP_200_OK
            )
        except (DispenserValueError, DispenserUsageValueError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ConnectionDataBaseError, RepositoryError) as e:
            return Response({"error": "Database or repository error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "Unexpected error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


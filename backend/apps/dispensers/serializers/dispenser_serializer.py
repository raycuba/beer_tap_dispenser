
from rest_framework import serializers

class CreateDispenserSerializer(serializers.Serializer):
    """
    Serializer Object para crear un dispenser.
    """
    flow_volume = serializers.FloatField(required=True, help_text="Litros por segundo que salen del grifo (ej: 0.064)")
    
    
class CreateDispenserResultSerializer(serializers.Serializer):
    """
    Serializer Object para el resultado de crear un dispenser.
    """
    id = serializers.UUIDField(read_only=True, help_text="ID relacionado con la base de datos")
    flow_volume = serializers.FloatField(help_text="Litros por segundo que salen del grifo (ej: 0.064)")
    
    
class ChangeDispenserSerializer(serializers.Serializer):
    """
    Serializer Object para cambiar un dispenser.
    """
    status = serializers.ChoiceField(required=True, choices=['open', 'close'], help_text="Estado actual del grifo")
    updated_at = serializers.DateTimeField(required=True, help_text="Fecha y hora de la última actualización del dispenser en formato ISO 8601 (ej: 2023-01-01T12:00:00Z)")
    
    
class DispenserDTOSerializer(serializers.Serializer):
    """
    Serializer Object para dispenser.
    """
    id = serializers.UUIDField(read_only=True, help_text="ID relacionado con la base de datos")
    flow_volume = serializers.FloatField(help_text="Litros por segundo que salen del grifo (ej: 0.064)")
    status = serializers.ChoiceField(choices=['open', 'close'], help_text="Estado actual del grifo")
# dispensers/models.py
from django.db import models
from django.utils import timezone
import uuid

class Dispenser(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('close', 'Close'),
    ]
    
    # Sobrescribimos el ID por defecto con un UUID por seguridad (evitar ID Enumeration)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Litros por segundo que salen del grifo (ej: 0.064)
    flow_volume = models.FloatField()  
    # Estado actual del grifo
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='close')

    def __str__(self):
        return f"Dispenser {self.id} ({self.status})"


class DispenserUsage(models.Model):
    # Relación 1:N -> Un dispensador puede tener muchos usos históricos
    # 'related_name' nos permite acceder desde el dispensador con: dispenser.usages.all()
    dispenser = models.ForeignKey(
        Dispenser, 
        on_delete=models.CASCADE, 
        related_name='usages'
    )
    opened_at = models.DateTimeField(auto_now_add=True) # Registra la fecha de creacion
    # Quedará en null mientras el asistente tenga el grifo abierto sirviéndose
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Guardamos una copia estática del flow_volume en el momento de la apertura.
    # Buenas prácticas: Si el administrador edita el flujo del dispensador mañana, 
    # los cálculos de los servicios de hoy no se corromperán.
    flow_volume = models.FloatField()

    @property
    def total_spent(self):
        """
        Calcula el dinero gastado en este uso específico.
        Precio de referencia exigido por la prueba: 12.25€ / litro.
        Soporta consultas en tiempo real incluso si el grifo sigue abierto.
        """
        PRICE_PER_LITER = 12.25
        
        # Si el grifo sigue abierto (closed_at es null), calculamos la duración hasta "ahora mismo"
        end_time = self.closed_at if self.closed_at else timezone.now()
        
        # Calculamos la diferencia en segundos (el float mantiene la precisión de los milisegundos)
        duration_seconds = (end_time - self.opened_at).total_seconds()
        
        # Evitamos problemas de sincronización de reloj de milisegundos negativos
        if duration_seconds < 0:
            duration_seconds = 0
            
        # Fórmula de la prueba: segundos * litros/segundo * precio/litro
        spent = duration_seconds * self.flow_volume * PRICE_PER_LITER
        
        # Redondeamos a 5 decimales para no perder precisión en la suma total posterior
        return round(spent, 5)

    def __str__(self):
        return f"Usage {self.id} - Dispenser {self.dispenser_id} ({self.total_spent}€)"
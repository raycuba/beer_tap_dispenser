// frontend/src/services/api.ts

/**
 * Interfaces y tipos para los endpoints de dispensadores
 */

export interface Dispenser {
  id: string;          // UUID generado por Django
  flow_volume: number; // Litros por segundo (ej: 0.064)
  status: 'open' | 'close';
  created_at?: string; // ISO timestamp
  updated_at?: string; // ISO timestamp
}

export interface DispenserUsage {
  id: string;
  dispenser_id: string;
  opened_at: string; // ISO timestamp
  closed_at?: string; // ISO timestamp nullable
  amount?: number | string; // El backend retorna como Decimal (string) para mantener precisión
}

export interface TotalSpentResult {
  dispenser_id: string;
  total_spent: number | string; // El backend retorna como Decimal (string) para mantener precisión
  usages: DispenserUsage[];
}

// URL base del backend desde variables de entorno
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Servicio centralizado para interactuar con la API de dispensadores
 * Maneja todas las operaciones CRUD y acciones especiales
 */
export const dispenserService = {
  
  /**
   * GET /api/dispensers/ - Obtiene la lista de todos los dispensadores
   */
  getAll: async (): Promise<Dispenser[]> => {
    const res = await fetch(`${API_BASE_URL}/api/dispensers/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store', // Evita caché para obtener datos en tiempo real
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.error || `Error al obtener dispensadores: ${res.status}`);
    }
    return res.json();
  },

  /**
   * GET /api/dispensers/{id}/ - Obtiene un dispensador específico por su ID
   */
  getById: async (id: string): Promise<Dispenser> => {
    if (!id) throw new Error('El ID del dispensador es requerido');
    
    const res = await fetch(`${API_BASE_URL}/api/dispensers/${id}/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
    });
    if (!res.ok) {
      if (res.status === 404) throw new Error(`Dispensador con ID ${id} no encontrado`);
      const error = await res.json().catch(() => ({}));
      throw new Error(error.error || `Error al obtener dispensador: ${res.status}`);
    }
    return res.json();
  },

  /**
   * POST /api/dispensers/ - Crea un nuevo dispensador
   */
  create: async (flowVolume: number): Promise<Dispenser> => {
    if (!flowVolume || flowVolume <= 0) {
      throw new Error('El flow_volume debe ser un número mayor a 0');
    }
    
    const res = await fetch(`${API_BASE_URL}/api/dispensers/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ flow_volume: flowVolume }),
    });
    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      throw new Error(error.error || `Error al crear dispensador: ${res.status}`);
    }
    return res.json();
  },

  /**
   * PUT /api/dispensers/{id}/ - Actualiza el estado de un dispensador (abierto/cerrado)
   * 
   * Nota: El backend requiere status y updated_at (timestamp UTC en formato ISO)
   */
  update: async (id: string, status: 'open' | 'close', updatedAt: string): Promise<Dispenser> => {
    if (!id) throw new Error('El ID del dispensador es requerido');
    if (!['open', 'close'].includes(status)) {
      throw new Error('El estado debe ser "open" o "close"');
    }
    if (!updatedAt) throw new Error('El timestamp actualizado es requerido');
    
    const res = await fetch(`${API_BASE_URL}/api/dispensers/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        status: status,
        updated_at: updatedAt
      }),
    });
    if (!res.ok) {
      if (res.status === 404) throw new Error(`Dispensador con ID ${id} no encontrado`);
      const error = await res.json().catch(() => ({}));
      throw new Error(error.error || `Error al actualizar dispensador: ${res.status}`);
    }
    return res.json();
  },

  /**
   * Métodos auxiliares para cambiar estado (wrapper más simple)
   */
  open: async (id: string): Promise<Dispenser> => {
    const now = new Date().toISOString();
    return dispenserService.update(id, 'open', now);
  },

  close: async (id: string): Promise<Dispenser> => {
    const now = new Date().toISOString();
    return dispenserService.update(id, 'close', now);
  },

  /**
   * DELETE /api/dispensers/{id}/ - Elimina un dispensador
   */
  delete: async (id: string): Promise<void> => {
    if (!id) throw new Error('El ID del dispensador es requerido');
    
    const res = await fetch(`${API_BASE_URL}/api/dispensers/${id}/`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) {
      if (res.status === 404) throw new Error(`Dispensador con ID ${id} no encontrado`);
      const error = await res.json().catch(() => ({}));
      throw new Error(error.error || `Error al eliminar dispensador: ${res.status}`);
    }
  },

  /**
   * GET /api/dispensers/get_total_spent_by_dispenser/{id}/ 
   * Obtiene el total gastado por un dispensador específico y su historial de uso
   */
  getTotalSpent: async (id: string): Promise<TotalSpentResult> => {
    if (!id) throw new Error('El ID del dispensador es requerido');
    
    const res = await fetch(`${API_BASE_URL}/api/dispensers/get_total_spent_by_dispenser/${id}/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store', // Para obtener datos actualizados en tiempo real
    });
    if (!res.ok) {
      if (res.status === 404) throw new Error(`Dispensador con ID ${id} no encontrado`);
      const error = await res.json().catch(() => ({}));
      throw new Error(error.error || `Error al obtener gasto total: ${res.status}`);
    }
    return res.json();
  }
};
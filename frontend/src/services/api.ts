// frontend/src/services/api.ts

// 1. Definimos las interfaces de TypeScript según tu base de datos
export interface Dispenser {
  id: string;          // El UUID que genera tu Django
  flow_volume: number; // Litros por segundo (ej: 0.064)
  status: 'open' | 'close';
}

export interface DispenserSpending {
  // Se adapta al JSON de tu endpoint: /api/dispensers/get_total_spent_by_dispenser/{id}/
  total_spent: number; 
}

// 2. Leemos la URL del backend desde las variables de entorno (.env.local)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 3. Centralizamos las llamadas HTTP usando el fetch nativo de Next.js
export const dispenserService = {
  
  // GET /api/dispensers/ -> Listar todos los grifos del festival
  getAll: async (): Promise<Dispenser[]> => {
    const res = await fetch(`${API_BASE_URL}/api/dispensers/`, {
      cache: 'no-store', // Crucial: evita datos obsoletos de caché para ver el estado real
    });
    if (!res.ok) throw new Error('Error al obtener los dispensadores');
    return res.json();
  },

  // POST /api/dispensers/ -> Crear un nuevo dispensador (Uso exclusivo de Admin)
  create: async (flowVolume: number): Promise<Dispenser> => {
    const res = await fetch(`${API_BASE_URL}/api/dispensers/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ flow_volume: flowVolume }),
    });
    if (!res.ok) throw new Error('Error al crear el dispensador');
    return res.json();
  },

  // PUT /api/dispensers/{id}/ -> Actualizar un grifo (Abrir o Cerrar)
  // Al ser un método PUT, le enviamos el objeto completo (status y flow_volume)
  changeStatus: async (id: string, status: 'open' | 'close', flowVolume: number): Promise<Dispenser> => {
    const res = await fetch(`${API_BASE_URL}/api/dispensers/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        status: status,
        flow_volume: flowVolume 
      }),
    });
    if (!res.ok) throw new Error('Error al actualizar el estado del dispensador');
    return res.json();
  },

  // GET /api/dispensers/get_total_spent_by_dispenser/{id}/ -> Consultar la recaudación del grifo
  getSpending: async (id: string): Promise<DispenserSpending> => {
    const res = await fetch(`${API_BASE_URL}/api/dispensers/get_total_spent_by_dispenser/${id}/`, {
      cache: 'no-store', // Para calcular el dinero al segundo si el grifo sigue abierto
    });
    if (!res.ok) throw new Error('Error al obtener el gasto total');
    return res.json();
  }
};
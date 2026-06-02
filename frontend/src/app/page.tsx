// frontend/src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { dispenserService, Dispenser } from '@/services/api';
import Link from 'next/link';

export default function Home() {
  const [dispensers, setDispensers] = useState<Dispenser[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingIds, setUpdatingIds] = useState<Set<string>>(new Set());
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loadError, setLoadError] = useState<string>('');

  // Cargar dispensadores al montar el componente
  useEffect(() => {
    const loadDispensers = async () => {
      try {
        setLoading(true);
        setLoadError('');
        console.log('Intentando obtener dispensadores...');
        const data = await dispenserService.getAll();
        console.log('Dispensadores obtenidos:', data);
        setDispensers(data);
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
        console.error('Error al cargar dispensadores:', errorMsg);
        setLoadError(errorMsg);
      } finally {
        setLoading(false);
      }
    };

    loadDispensers();
  }, []);

  // Manejar cambio de estado (abrir/cerrar)
  const handleToggleStatus = async (dispenser: Dispenser) => {
    const { id, status } = dispenser;
    const newStatus = status === 'open' ? 'close' : 'open';

    // Agregar ID a los que se están actualizando
    setUpdatingIds(prev => new Set([...prev, id]));
    setErrors(prev => ({ ...prev, [id]: '' }));

    try {
      // Llamar a la API según el nuevo estado
      const updatedDispenser = newStatus === 'open' 
        ? await dispenserService.open(id)
        : await dispenserService.close(id);

      // Actualizar el dispensador en la lista local
      setDispensers(prevDispensers =>
        prevDispensers.map(d => d.id === id ? updatedDispenser : d)
      );
    } catch (err) {
      // Manejar error y almacenar el mensaje
      const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
      setErrors(prev => ({ ...prev, [id]: errorMsg }));
      console.error(`Error al actualizar dispensador ${id}:`, err);
    } finally {
      // Remover ID de los que se están actualizando
      setUpdatingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen flex-col items-center justify-center text-xl bg-gray-900 text-white">
        <div className="animate-spin rounded-full h-12 w-12 border border-amber-500 border-t-transparent mb-4"></div>
        <p>Cargando grifos...</p>
        <p className="text-sm text-gray-400 mt-2">(API: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'})</p>
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="flex h-screen flex-col items-center justify-center bg-gray-900 text-white p-8">
        <div className="max-w-md">
          <p className="text-3xl mb-4">❌</p>
          <h1 className="text-2xl font-bold mb-4">Error al conectar con la API</h1>
          <div className="bg-red-500/10 border border-red-500 text-red-400 p-4 rounded mb-6">
            <p className="text-sm">{loadError}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded mb-6 text-sm text-gray-300">
            <p className="font-semibold mb-2">Información de depuración:</p>
            <ul className="space-y-1">
              <li>• API URL: <code className="bg-gray-700 px-2 py-1 rounded">{process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}</code></li>
              <li>• Endpoint: <code className="bg-gray-700 px-2 py-1 rounded">/api/dispensers/</code></li>
              <li>• Verifica que el backend Django esté ejecutándose</li>
            </ul>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="w-full bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded font-medium transition-colors"
          >
            🔄 Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-900 p-8 text-white">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-amber-500">🍺 Beer Tap Festival Dashboard</h1>
          <Link
            href="/admin"
            className="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded font-medium transition-colors"
          >
            ⚙️ Panel de Admin
          </Link>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {dispensers.length === 0 ? (
            <p className="text-gray-400">No hay dispensadores instalados en la base de datos.</p>
          ) : (
            dispensers.map((dispenser) => (
              <div key={dispenser.id} className="bg-gray-800 p-6 rounded-lg border border-gray-700">
                <p className="text-sm text-gray-400 truncate">ID: {dispenser.id}</p>
                <p className="text-lg my-2">Flujo: <span className="font-mono text-amber-400">{dispenser.flow_volume} L/s</span></p>
                
                <div className="mt-4 flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                    dispenser.status === 'open' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                  }`}>
                    {dispenser.status}
                  </span>
                  
                  <button
                    onClick={() => handleToggleStatus(dispenser)}
                    disabled={updatingIds.has(dispenser.id)}
                    className="bg-amber-600 hover:bg-amber-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-4 py-2 rounded font-medium transition-colors"
                  >
                    {updatingIds.has(dispenser.id) ? (
                      <span className="flex items-center gap-2">
                        <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Procesando...
                      </span>
                    ) : (
                      dispenser.status === 'open' ? 'Cerrar Grifo' : 'Abrir Grifo'
                    )}
                  </button>
                </div>

                {/* Mostrar mensaje de error si existe */}
                {errors[dispenser.id] && (
                  <p className="mt-3 text-sm text-red-400 bg-red-500/10 p-2 rounded">
                    ⚠️ {errors[dispenser.id]}
                  </p>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
}
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { dispenserService, Dispenser, TotalSpentResult } from '@/services/api';
import { authService, AdminSession } from '@/services/auth';
import Link from 'next/link';

export default function AdminPage() {
  const router = useRouter();
  
  // 1. TODOS LOS STATES PRIMERO
  const [session, setSession] = useState<AdminSession | null>(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [dispensers, setDispensers] = useState<Dispenser[]>([]);
  const [loading, setLoading] = useState(true);
  const [formLoading, setFormLoading] = useState(false);
  const [flowVolume, setFlowVolume] = useState('');
  const [deleteLoading, setDeleteLoading] = useState<Set<string>>(new Set());
  const [selectedDispenserId, setSelectedDispenserId] = useState<string | null>(null);
  const [spendingData, setSpendingData] = useState<TotalSpentResult | null>(null);
  const [spendingLoading, setSpendingLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');

  // 2. TODOS LOS USEEFFECT JUNTOS E INCONDICIONALES ARRIBA

  // Verificar autenticación al cargar
  useEffect(() => {
    const currentSession = authService.getCurrentSession();
    if (!currentSession) {
      router.push('/admin/login');
    } else {
      setSession(currentSession);
      setAuthLoading(false);
    }
  }, [router]);

  // Cargar dispensadores al montar el componente (¡Movido aquí arriba!)
  useEffect(() => {
    // Solo intentamos cargar si ya ha pasado el filtro de autenticación inicial
    // para evitar llamadas fantasmas al backend si no hay sesión activa
    const currentSession = authService.getCurrentSession();
    if (currentSession) {
      loadDispensers();
    }
  }, []);

  // 3. MÉTODOS Y FUNCIONES LÓGICAS

  const loadDispensers = async () => {
    try {
      setLoading(true);
      const data = await dispenserService.getAll();
      setDispensers(data);
      setError('');
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    router.push('/admin/login');
  };

  const handleCreateDispenser = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!flowVolume || parseFloat(flowVolume) <= 0) {
      setError('El flow_volume debe ser un número mayor a 0');
      return;
    }

    try {
      setFormLoading(true);
      setError('');
      await dispenserService.create(parseFloat(flowVolume));
      setSuccessMessage('✅ Dispensador creado exitosamente');
      setFlowVolume('');
      await loadDispensers();
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMsg);
    } finally {
      setFormLoading(false);
    }
  };

  const handleDeleteDispenser = async (id: string) => {
    if (!confirm('¿Estás seguro de que deseas eliminar este dispensador?')) return;

    try {
      setDeleteLoading(prev => new Set([...prev, id]));
      setError('');
      await dispenserService.delete(id);
      setSuccessMessage('✅ Dispensador eliminado exitosamente');
      await loadDispensers();
      
      if (selectedDispenserId === id) {
        setSelectedDispenserId(null);
        setSpendingData(null);
      }
      
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMsg);
    } finally {
      setDeleteLoading(prev => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  const handleViewSpending = async (id: string) => {
    try {
      setSpendingLoading(true);
      setError('');
      const data = await dispenserService.getTotalSpent(id);
      setSelectedDispenserId(id);
      setSpendingData(data);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMsg);
      setSelectedDispenserId(null);
      setSpendingData(null);
    } finally {
      setSpendingLoading(false);
    }
  };

  const closeSpendingModal = () => {
    setSelectedDispenserId(null);
    setSpendingData(null);
  };

  // 4. LAS SALIDAS TEMPRANAS (RETURNS) ABAJO DE LOS HOOKS

  if (authLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-900 text-white">
        <div className="animate-spin rounded-full h-12 w-12 border border-amber-500 border-t-transparent"></div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  // 5. RENDERIZADO PRINCIPAL
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header unificado (eliminado el duplicado) */}
      <header className="bg-gray-800 border-b border-gray-700 p-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-amber-500">🍺 Administración de Grifos</h1>
            <p className="text-gray-400 mt-1">Panel de control para gestionar los dispensadores del festival</p>
            <p className="text-sm text-amber-400 mt-2">👤 Usuario: <span className="font-semibold">{session.username}</span></p>
          </div>
          <div className="flex gap-3">
            <Link 
              href="/" 
              className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded font-medium transition-colors"
            >
              ← Dashboard
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-500 px-4 py-2 rounded font-medium transition-colors"
            >
              🚪 Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 space-y-8">
        
        {/* Mensajes de error y éxito */}
        {error && (
          <div className="bg-red-500/10 border border-red-500 text-red-400 p-4 rounded-lg flex items-start gap-3">
            <span className="text-xl">⚠️</span>
            <p>{error}</p>
          </div>
        )}
        
        {successMessage && (
          <div className="bg-green-500/10 border border-green-500 text-green-400 p-4 rounded-lg flex items-start gap-3">
            <span className="text-xl">✅</span>
            <p>{successMessage}</p>
          </div>
        )}

        {/* Formulario para crear dispensador */}
        <section className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold text-amber-400 mb-6">➕ Crear Nuevo Dispensador</h2>
          <form onSubmit={handleCreateDispenser} className="flex gap-4 items-end">
            <div className="flex-1">
              <label htmlFor="flowVolume" className="block text-sm font-medium text-gray-300 mb-2">
                Flow Volume (L/s)
              </label>
              <input
                id="flowVolume"
                type="number"
                step="0.001"
                min="0"
                placeholder="Ej: 0.064"
                value={flowVolume}
                onChange={(e) => setFlowVolume(e.target.value)}
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 text-white rounded focus:outline-none focus:border-amber-500"
              />
            </div>
            <button
              type="submit"
              disabled={formLoading}
              className="bg-amber-600 hover:bg-amber-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-6 py-2 rounded font-medium transition-colors"
            >
              {formLoading ? 'Creando...' : 'Crear'}
            </button>
          </form>
        </section>

        {/* Tabla de dispensadores */}
        <section className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-2xl font-bold text-amber-400 mb-6">📋 Dispensadores Registrados</h2>
          
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border border-amber-500 border-t-transparent"></div>
            </div>
          ) : dispensers.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No hay dispensadores registrados</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="px-4 py-3 text-sm font-semibold text-gray-300">ID</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-300">Flow Volume</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-300">Estado</th>
                    <th className="px-4 py-3 text-sm font-semibold text-gray-300">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {dispensers.map((dispenser, index) => (
                    <tr key={`${dispenser.id}-${index}`} className="hover:bg-gray-700/50 transition-colors">
                      <td className="px-4 py-3 text-sm font-mono text-gray-300 truncate max-w-xs">{dispenser.id}</td>
                      <td className="px-4 py-3 text-sm text-amber-400 font-mono">{dispenser.flow_volume}</td>
                      <td className="px-4 py-3 text-sm">
                        <span className={`px-2 py-1 rounded-full text-xs font-bold uppercase ${
                          dispenser.status === 'open' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                        }`}>
                          {dispenser.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm space-x-2">
                        <button
                          onClick={() => handleViewSpending(dispenser.id)}
                          className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded text-xs font-medium transition-colors"
                        >
                          💰 Ver Gasto
                        </button>
                        <button
                          onClick={() => handleDeleteDispenser(dispenser.id)}
                          disabled={deleteLoading.has(dispenser.id)}
                          className="bg-red-600 hover:bg-red-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-3 py-1 rounded text-xs font-medium transition-colors"
                        >
                          {deleteLoading.has(dispenser.id) ? '⏳' : '🗑️'} Eliminar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Modal de historial de gasto */}
        {selectedDispenserId && spendingData && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-gray-800 border border-gray-700 rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <div className="sticky top-0 bg-gray-800 border-b border-gray-700 p-6 flex justify-between items-center">
                <h3 className="text-xl font-bold text-amber-400">
                  💰 Historial de Gasto
                </h3>
                <button
                  onClick={closeSpendingModal}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  ✕
                </button>
              </div>

              <div className="p-6 space-y-6">
                <div className="bg-gray-700/50 p-4 rounded border border-gray-600">
                  <p className="text-sm text-gray-400">Total Gastado</p>
                  <p className="text-3xl font-bold text-amber-400">
                    {parseFloat(String(spendingData.total_spent)).toFixed(2)}€
                  </p>
                </div>

                {/* Si tienes un array de consumos en tu API, se pintará aquí */}
                {/* Nota: Adaptado para evitar romper si `usages` no viene del backend */}
                <div>
                  <h4 className="text-lg font-semibold text-gray-300 mb-4">Historial de Uso</h4>
                  {spendingData.usages && spendingData.usages.length > 0 ? (
                    <div className="space-y-3">
                      {spendingData.usages.map((usage, index) => (
                        <div key={`${usage.opened_at}-${index}`} className="bg-gray-700/50 p-3 rounded border border-gray-600">
                          <div className="flex justify-between items-start">
                            <div>
                              <p className="text-sm text-gray-400">
                                Abierto: {new Date(usage.opened_at).toLocaleString('es-ES')}
                              </p>
                              {usage.closed_at && (
                                <p className="text-sm text-gray-400">
                                  Cerrado: {new Date(usage.closed_at).toLocaleString('es-ES')}
                                </p>
                              )}
                              <p className="text-sm text-amber-400 font-semibold mt-1">
                                Total: {parseFloat(String(usage.total_spent)).toFixed(2)}€
                              </p>
                            </div>
                            {!usage.closed_at && (
                              <span className="bg-green-500/20 text-green-400 px-2 py-1 rounded text-xs font-bold">
                                ABIERTO
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-400 text-center py-4">No hay historial de uso disponible</p>
                  )}
                </div>
              </div>

              <div className="border-t border-gray-700 p-6 bg-gray-700/30">
                <button
                  onClick={closeSpendingModal}
                  className="w-full bg-gray-600 hover:bg-gray-500 text-white py-2 rounded font-medium transition-colors"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
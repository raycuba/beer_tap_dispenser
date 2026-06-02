// frontend/src/app/page.tsx
'use client';

import { useEffect, useState } from 'react';
import { dispenserService, Dispenser } from '@/services/api';

export default function Home() {
  const [dispensers, setDispensers] = useState<Dispenser[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dispenserService.getAll()
      .then(data => {
        setDispensers(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="flex h-screen items-center justify-center text-xl">Cargando grifos...</div>;
  }

  return (
    <main className="min-h-screen bg-gray-900 p-8 text-white">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-amber-500">🍺 Beer Tap Festival Dashboard</h1>
        
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
                  <button className="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded font-medium transition-colors">
                    {dispenser.status === 'open' ? 'Cerrar Grifo' : 'Abrir Grifo'}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
}
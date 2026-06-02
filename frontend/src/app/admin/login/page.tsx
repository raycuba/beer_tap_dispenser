'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';

export default function AdminLoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!username || !password) {
      setError('Usuario y contraseña son requeridos');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const success = await authService.login(username, password);
      
      if (success) {
        // Redirigir al panel de admin
        router.push('/admin');
      } else {
        setError('Usuario o contraseña incorrectos');
        setPassword('');
      }
    } catch (err) {
      setError('Error al intentar iniciar sesión');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo/Título */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-amber-500 mb-2">🍺</h1>
          <h2 className="text-3xl font-bold text-white mb-2">Beer Tap Festival</h2>
          <p className="text-gray-400">Panel de Administración</p>
        </div>

        {/* Formulario */}
        <form
          onSubmit={handleLogin}
          className="bg-gray-800 border border-gray-700 rounded-lg p-8 shadow-2xl"
        >
          <div className="space-y-6">
            {/* Usuario */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                Usuario
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
                placeholder="Ingresa tu usuario"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 text-white rounded focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 disabled:opacity-50"
              />
            </div>

            {/* Contraseña */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Contraseña
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                placeholder="Ingresa tu contraseña"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 text-white rounded focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 disabled:opacity-50"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !loading) {
                    handleLogin(e as any);
                  }
                }}
              />
            </div>

            {/* Mensaje de error */}
            {error && (
              <div className="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded text-sm">
                ⚠️ {error}
              </div>
            )}

            {/* Botón de login */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-amber-600 hover:bg-amber-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded transition-colors"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Ingresando...
                </span>
              ) : (
                'Ingresar'
              )}
            </button>
          </div>
        </form>

        {/* Información de demo */}
        <div className="mt-8 bg-blue-500/10 border border-blue-500 rounded-lg p-4">
          <p className="text-blue-400 text-sm font-medium mb-2">📝 Credenciales de Demo:</p>
          <ul className="text-blue-300 text-xs space-y-1">
            <li>• Usuario: <code className="bg-blue-900 px-2 py-0.5 rounded">admin</code> | Contraseña: <code className="bg-blue-900 px-2 py-0.5 rounded">admin123</code></li>
            <li>• Usuario: <code className="bg-blue-900 px-2 py-0.5 rounded">manager</code> | Contraseña: <code className="bg-blue-900 px-2 py-0.5 rounded">manager123</code></li>
          </ul>
        </div>
      </div>
    </div>
  );
}

/**
 * Servicio de autenticación para el panel de admin
 * Usuarios y contraseñas fijas
 */

// Lista de usuarios y contraseñas válidas
const VALID_USERS = [
  { username: 'admin', password: 'admin123' },
  { username: 'manager', password: 'manager123' },
];

const SESSION_KEY = 'beer_tap_admin_session';

export interface AdminSession {
  username: string;
  loginTime: number;
}

/**
 * Validar credenciales contra la lista de usuarios
 */
export const authService = {
  login: async (username: string, password: string): Promise<boolean> => {
    // Simular delay de red
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const user = VALID_USERS.find(u => u.username === username && u.password === password);
    
    if (user) {
      // Guardar sesión en localStorage
      const session: AdminSession = {
        username: user.username,
        loginTime: Date.now(),
      };
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      return true;
    }
    return false;
  },

  logout: () => {
    localStorage.removeItem(SESSION_KEY);
  },

  getCurrentSession: (): AdminSession | null => {
    if (typeof window === 'undefined') return null;
    
    try {
      const session = localStorage.getItem(SESSION_KEY);
      return session ? JSON.parse(session) : null;
    } catch {
      return null;
    }
  },

  isAuthenticated: (): boolean => {
    return authService.getCurrentSession() !== null;
  },
};

# 🔐 Autenticación - Panel de Administración

## Credenciales de Acceso

El panel de administración en `/admin` requiere autenticación con usuario y contraseña. Existen dos usuarios predeterminados:

### Usuario 1: Admin
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Usuario 2: Manager
- **Usuario**: `manager`
- **Contraseña**: `manager123`

---

## Cómo funciona la autenticación

1. **Acceso sin autenticación**: Si intentas acceder a `/admin` sin estar logueado, serás redirigido a `/admin/login`
2. **Página de login**: Ingresa cualquiera de los usuarios y contraseñas anteriores
3. **Sesión activa**: Una vez autenticado, tu sesión se guarda en localStorage
4. **Logout**: Haz clic en el botón "🚪 Cerrar Sesión" en la esquina superior derecha del panel

---

## Cambiar credenciales

Si deseas cambiar los usuarios y contraseñas, edita el archivo:
```
frontend/src/services/auth.ts
```

Busca la lista `VALID_USERS`:
```typescript
const VALID_USERS = [
  { username: 'admin', password: 'admin123' },
  { username: 'manager', password: 'manager123' },
];
```

Puedes agregar, eliminar o modificar usuarios según necesites.

---

## Notas de seguridad

⚠️ **IMPORTANTE**: Esta es una autenticación básica local para desarrollo/demo. 

**Para producción, deberías:**
- Usar autenticación del backend (JWT, OAuth, etc.)
- No guardar credenciales en el código frontend
- Usar HTTPS
- Implementar refresh tokens
- Agregar rate limiting en el backend

---

## Rutas protegidas

- `/admin` - Panel de administración (requiere autenticación)
- `/admin/login` - Página de login (acceso público)
- `/` - Dashboard (acceso público)


# 🍺 Beer Tap Dispenser - Guía de Inicio

## Requisitos previos
- **Backend**: Python 3.12.8, Django
- **Frontend**: Node.js 18+, npm/yarn
- **Base de datos**: postgres:15-alpine (incluida)

---

## 🚀 Iniciar el Proyecto

### 1️⃣ Backend (Django)

```bash
# Navegar al directorio backend
cd backend

# Activar el entorno virtual
source ../.venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar el servidor
python manage.py runserver
```

El backend estará disponible en:
Documentacion de la API en: http://127.0.0.1:8000/docs/
Panel de Admin en: http://127.0.0.1:8000/admin/
    credenciales del admin: 
        username: 'admin', password: 'back9878'


### 2️⃣ Frontend (Next.js)

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Verificar que .env.local tenga la URL correcta del backend
cat .env.local
# Debe mostrar: NEXT_PUBLIC_API_URL=http://localhost:8000

# Iniciar el servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:3000**

    credenciales de administracion del frontend:
        username: 'admin', password: 'admin123' 
        username: 'manager', password: 'manager123' 

---

### INICIAR EL SERVIDOR DESDE DOCKER: ----------------------------------------------------------------------------------------------
Asegúrate de apagar cualquier proceso local de Django, Next o Postgres que tengas corriendo en tu máquina para liberar los puertos.

## Ve a la raíz del proyecto y ejecuta:
Bash
docker-compose up --build

## Una vez que veas en los logs que los tres contenedores están activos:
abre otra terminal y ejecuta las migraciones dentro del contenedor de Django para poblar las tablas por primera vez:

Bash
docker-compose exec backend python manage.py migrate

## Para crear una contraseña para acceder al admin del backend:
abre otra terminal y ejecuta 

Bash 
docker-compose exec backend python manage.py createsuperuser


¡Y listo! Al abrir http://localhost:3000 tendrás tu Next.js controlando el backend de Django, guardando todo en el Postgres aislado. 

Acceso a las aplicaciones:

    Frontend (Dashboard): http://localhost:3000

    Backend (API REST): http://localhost:8000/docs/
    Backend (ADMIN): http://127.0.0.1:8000/admin/

## 🔍 Solución de problemas -----------------------------------------------------------------------------------------------------------------

### ❌ "Cargando grifos..." infinito

**Causas comunes:**
1. El backend Django no está ejecutándose
2. La URL del backend es incorrecta
3. CORS no está configurado correctamente

**Soluciones:**

✅ **Verificar que Django esté corriendo:**
```bash
curl http://localhost:8000/api/dispensers/
```

✅ **Revisar la consola del navegador:**
- Abre DevTools (F12)
- Ve a la pestaña **Console**
- Busca mensajes de error
- Verifica la URL del API que se muestra

✅ **Reiniciar Next.js después de cambiar .env.local:**
- Detén `npm run dev`
- Elimina la carpeta `.next`
- Vuelve a ejecutar `npm run dev`

✅ **Verificar CORS en Django:**
Si ves errores CORS, asegúrate de que en `backend/config/settings.py` esté:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## 📍 Rutas disponibles

- **Dashboard**: http://localhost:3000/
- **Panel de Admin**: http://localhost:3000/admin

---

## 🛠️ Comandos útiles

### Backend
```bash
# Crear superusuario (opcional, para admin)
python manage.py createsuperuser

# Ver logs detallados
python manage.py runserver --verbosity 2
```

### Frontend
```bash
# Compilar para producción
npm run build

# Iniciar servidor de producción
npm start
```

---

### Reiniciar todo el proyecto:
Limpiar solo este proyecto (La más recomendada)
Si solo quieres reiniciar el dispenser de cerveza sin afectar a otros proyectos de Docker que tengas en tu ordenador, 
ejecuta este comando en la raíz (donde está el docker-compose.yml):

    Bash
    docker-compose down -v --rmi all

    ¿Qué hace exactamente este comando?
        down: Detiene y elimina los contenedores y la red virtual del proyecto.
        -v (o --volumes): Borra el volumen de PostgreSQL. Esto destruirá los datos de las tablas para que la base de datos comience totalmente vacía.
        --rmi all: Elimina las imágenes locales que se compilaron para el backend y el frontend. Así forzarás a Docker a reinstalar el requirements.txt y el package.json desde cero la próxima vez.

## 📝 Notas importantes

- El archivo `.env.local` contiene variables sensibles, **no commitear a Git**
- Está en `.gitignore` por defecto
- Los cambios en `.env.local` requieren reiniciar el servidor de Next.js
- Los decimales del backend se envían como strings (precaución de precisión)

---

¡Si aún tienes problemas, revisa la consola del navegador (F12) y verás el mensaje de error exacto! 🔍

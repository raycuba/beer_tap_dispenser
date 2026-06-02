# 🍺 Beer Tap Dispenser - Guía de Inicio

## Requisitos previos

- **Backend**: Python 3.9+, Django
- **Frontend**: Node.js 18+, npm/yarn
- **Base de datos**: SQLite (incluida)

---

## 🚀 Iniciar el Proyecto

### 1️⃣ Backend (Django)

```bash
# Navegar al directorio backend
cd backend

# Activar el entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar el servidor
python manage.py runserver
```

El backend estará disponible en: **http://localhost:8000**

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

---

## 🔍 Solución de problemas

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

## 📝 Notas importantes

- El archivo `.env.local` contiene variables sensibles, **no commitear a Git**
- Está en `.gitignore` por defecto
- Los cambios en `.env.local` requieren reiniciar el servidor de Next.js
- Los decimales del backend se envían como strings (precaución de precisión)

---

¡Si aún tienes problemas, revisa la consola del navegador (F12) y verás el mensaje de error exacto! 🔍

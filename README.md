# Beer Tap Dispenser API & Dashboard

Este proyecto implementa el MVP para la gestión de dispensadores de cerveza en un festival, permitiendo el control del flujo de consumiciones tanto para asistentes (anónimos) como para el administrador. El sistema calcula los costes en tiempo real de manera *stateless* basándose en timestamps de apertura y cierre.

## Arquitectura Utilizada
- **Backend:** Django REST Framework aplicando principios de **Domain-Driven Design (DDD)** para aislar las reglas de negocio, entidades de dominio y servicios.
- **Frontend:** Next.js 16 con **TypeScript** y **Tailwind CSS**, gestionando el control de accesos de administrador a nivel de cliente de acuerdo a las especificaciones de la prueba.
- **Persistencia:** PostgreSQL.

## Requisitos Previos
Tener instalado [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/).

## Instrucciones de Despliegue Rápido

1. **Clonar el repositorio y situarse en la raíz del proyecto:**
   ```bash
   cd beer_tap_dispenser

## INICIAR EL SERVIDOR DESDE DOCKER: ----------------------------------------------------------------------------------------------
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


## Para otras dudas tecnicas 
revisar el archivo SETUP.md

# 📦 Proyecto FastAPI + NiceGUI + PostgreSQL

Este proyecto está construido con:

- ✅ **FastAPI** como backend (API REST)
- ✅ **SQLModel** como ORM de la BD
- ✅ **NiceGUI** como interfaz de usuario (frontend)
- ✅ **PostgreSQL** como base de datos relacional

---

## 📁 Estructura general del proyecto

```
mi_proyecto/
├── app/
│   ├── main.py                             # Punto de entrada que monta FastAPI + NiceGUI

│   ├── backend/                            # Toda la lógica del servidor
│   │   ├── api/                            # Endpoints y protección con JWT
│   │   │   ├── routes/
│   │   │   │   ├── users.py                # Rutas de usuarios (perfil, CRUD)
│   │   │   │   ├── events.py               # Rutas de eventos
│   │   │   │   └── auth.py                 # Login, registro, autenticación
│   │   │   └── dependencies/
│   │   │       └── auth_guard.py           # Verificación JWT (get_current_user) - Actua como Middleware

│   │   ├── db/                             # Conexión y consultas SQL a la base de datos
│   │   │   ├── db_handler.py               # Conexión y gestión de PostgreSQL

│   │   ├── models/                         # Modelos SQLModel para BD y validación
│   │   │   ├── user
|   |   |   |     ├── user.py               # Modelo de usuario según la BD
|   |   |   |     └── DTOs                  # Carpeta para los DTOs del usuario
│   │   │   ├── event
|   |   |   |     ├── event.py
|   |   |   |     └── DTOs

│   │   ├── services/                       # Lógica de negocio (sin lógica en rutas)
│   │   │   ├── user_service.py             # Registro, login, perfil, etc.

│   │   └── utils/                          # Funciones auxiliares reutilizables
│   │       ├── jwt.py                      # Crear y verificar tokens JWT
│   │       └── hashing.py                  # Hashing de contraseñas (bcrypt)

│   ├── frontend/                           # Interfaz de usuario con NiceGUI
│   │   ├── routes/                         # Páginas visibles
│   │   │   ├── home.py
│   │   │   ├── dashboard.py
│   │   │   └── login.py
│   │   ├── components/                     # Componentes visuales reutilizables
│   │   │   ├── navbar.py
│   │   │   ├── sidebar.py
│   │   │   └── user_card.py
│   │   ├── static/
│   │   │   ├── img/

    ├── requirements.in                     # Lista las dependencias directas del proyecto, sin versiones estrictas.
    ├── requirements.txt                    # Versión bloqueada con todas las dependencias y sub-dependencias.
├── .env                                    # Variables secretas (BD, JWT_SECRET, etc.)
```

---

## 🧠 ¿Para qué sirve cada carpeta?

| Carpeta / Archivo           | Descripción                                                 |
|-----------------------------|-------------------------------------------------------------|
| `app/main.py`               | Punto de entrada que lanza FastAPI y la app de NiceGUI      |
| `app/backend/api/routes/`   | Endpoints que el cliente puede llamar                       |
| `app/backend/db/`           | Lógica de conexión y consultas SQL a la base de datos       |
| `app/backend/models/`       | Modelos SQLModel para tablas y validación de datos          |
| `app/backend/services/`     | Lógica de negocio (validaciones, operaciones complejas)     |
| `app/backend/utils/`        | Funciones auxiliares reutilizables (JWT, hashing, etc.)     |
| `app/frontend/routes/`      | Páginas visibles del frontend (home, login, dashboard)      |
| `app/frontend/components/`  | Componentes NiceGUI reutilizables (navbar, tarjetas, etc.)  |
| `app/requirements.txt`      | Lista de dependencias necesarias del proyecto               |
| `.env`                      | Variables privadas como credenciales y secretos             |

---

## Guía para gestionar paquetes con piptools

> Antes de usar `pip-compile`, asegúrate de tener `pip-tools` instalado:
>     - Ejecuta `pip install pip-tools`

1. **Cuando necesites añadir un nuevo paquete:**  
   - Añádelo en `requirements.in`  
   - Ejecuta `py -m piptools compile requirements.in` para actualizar `requirements.txt`  
   - Ejecuta `py -m pip install -r requirements.txt` para instalar el nuevo paquete  

2. **Para actualizar paquetes existentes:**  
   - Actualiza la versión en `requirements.in` (o elimina la versión para obtener la más reciente)  
   - Ejecuta `py -m piptools compile requirements.in`  
   - Ejecuta `py -m pip install -r requirements.txt`  

3. **Para instalar dependencias en una máquina nueva:**  
   - Simplemente ejecuta `py -m pip install -r requirements.txt`  

> Este sistema garantiza que:  
> - Las dependencias estén correctamente registradas  
> - Todas las sub-dependencias estén bloqueadas a versiones específicas  
> - El entorno sea reproducible en diferentes máquinas  
> - Tengas una distinción clara entre las dependencias directas (en `.in`) y todas las dependencias (en `.txt`)  

--

## ✅ Buenas prácticas internas

- Las rutas **solo deben recibir y responder** datos, sin lógica pesada.  
- Toda la lógica de negocio debe estar en los servicios.  
- Las consultas SQL deben estar separadas en archivos específicos.  
- Las rutas privadas deben usar `Depends(get_current_user)` de el auth_guard para protección.  
- No conectar directamente a la base de datos desde los endpoints.  
- No incluir lógica de negocio dentro de las rutas.  

---

Si tienes dudas, grita, no importa.  
Este README es nuestra brújula. 🧭

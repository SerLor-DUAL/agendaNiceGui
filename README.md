# 📦 Proyecto FastAPI + NiceGUI + PostgreSQL

Este proyecto está construido con:

- ✅ **FastAPI** como backend (API REST)
- ✅ **NiceGUI** como interfaz de usuario (frontend)
- ✅ **PostgreSQL** como base de datos relacional

---

## 📁 Estructura general del proyecto

```
mi_proyecto/
├── app/
│   ├── main.py                       # Punto de entrada que monta FastAPI + NiceGUI
│   ├── __init__.py

│
│   ├── backend/                      # Toda la lógica del servidor
│   │   ├── api/                      # Endpoints y protección con JWT
│   │   │   ├── routes/
│   │   │   │   ├── users.py          # Rutas de usuarios (perfil, CRUD)
│   │   │   │   ├── auth.py           # Login, registro, autenticación
│   │   │   │   └── data.py           # Rutas generales (dashboard, otros datos)
│   │   │   └── dependencies/
│   │   │       └── auth_guard.py     # Verificación de JWT (get_current_user)

│   │   ├── db/                       # Conexión y consultas SQL a la BD
│   │   │   ├── db_handler.py         # Conecta y gestiona PostgreSQL
│   │   │   ├── user_queries.py       # SQL relacionado con usuarios
│   │   │   └── data_queries.py       # SQL para otros datos

│   │   ├── services/                 # Lógica del backend (no meterla en las rutas)
│   │   │   ├── user_service.py       # Registro, login, perfil, etc.
│   │   │   └── data_service.py       # Datos generales, dashboard, etc.

│   │   └── utils/                    # Funciones auxiliares reutilizables
│   │       ├── jwt.py                # Crear/verificar tokens JWT
│   │       └── hashing.py            # Hashing de contraseñas (bcrypt)

│
│   ├── frontend/                     # Interfaz de usuario NiceGUI
│   │   ├── routes/                   # Páginas visibles
│   │   │   ├── home.py
│   │   │   ├── dashboard.py
│   │   │   └── login.py
│   │   ├── components/               # Componentes visuales reutilizables
│   │   │   ├── navbar.py
│   │   │   ├── sidebar.py
│   │   │   └── user_card.py
│   │   └── __init__.py

├── requirements.txt                 # Librerías necesarias (FastAPI, NiceGUI, psycopg, etc.)
├── .env                             # Variables secretas (DB, JWT_SECRET, etc.)
```

---

## 🧠 ¿Para qué sirve cada carpeta?

| Carpeta / Archivo         | ¿Qué contiene y para qué sirve? |
|---------------------------|----------------------------------|
| `main.py`                 | Lanza el servidor FastAPI y la app de NiceGUI |
| `backend/api/routes/`     | Los endpoints que el cliente puede llamar |
| `backend/db/`             | Toda la lógica relacionada con la base de datos (conexión y SQLs) |
| `backend/services/`       | Lógica de negocio (ej. comprobar login, procesar datos, etc.) |
| `backend/utils/`          | Funciones auxiliares reutilizables (JWT, hashing, etc.) |
| `frontend/routes/`        | Páginas visibles del frontend (home, login, dashboard) |
| `frontend/components/`    | Componentes NiceGUI reutilizables (barra lateral, tarjetas, etc.) |
| `.env`                    | Variables privadas como credenciales y secretos |
| `requirements.txt`        | Librerías necesarias para que funcione el proyecto |

---

## ✅ Buenas prácticas internas

- ✅ Las rutas solo deben recibir y responder (sin lógica pesada dentro)
- ✅ Toda la lógica se gestiona en los servicios
- ✅ Las consultas SQL están separadas por archivo
- ✅ Las rutas privadas deben usar `Depends(get_current_user)`
- ❌ No conectes directamente a la base desde los endpoints
- ❌ No metas lógica de negocio en `routes/`

---

Si tienes dudas, grita, no importa.  
Este README es nuestra brújula. 🧭
# AgendaNiceGUI - Detailed Project Analysis & Specifications

## 📋 Project Overview

**AgendaNiceGUI** is a modern web-based calendar/agenda application built with a hybrid architecture combining:

- **Backend**: FastAPI (Python) with PostgreSQL database
- **Frontend**: NiceGUI (Python-based web UI framework)
- **Architecture**: Full-stack monolithic application with clear separation of concerns

## 🏗️ Architecture & Technology Stack

### Core Technologies

- **FastAPI**: REST API backend with automatic documentation
- **NiceGUI**: Python-based web UI framework (alternative to traditional JavaScript frameworks)
- **PostgreSQL**: Relational database with AsyncPG driver
- **SQLModel**: Modern ORM combining SQLAlchemy and Pydantic
- **JWT**: Token-based authentication with HTTP-only cookies
- **Tailwind CSS**: Utility-first CSS framework for styling

### Key Libraries

- `asyncpg` - Async PostgreSQL driver
- `python-jose[cryptography]` - JWT token handling
- `passlib` - Password hashing with bcrypt
- `python-multipart` - File upload support
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client

## 📁 Project Structure Analysis

**Authentication System**

1. **JWT-based authentication** with access and refresh tokens
2. **HTTP-only cookies** for secure token storage
3. **Password hashing** using bcrypt
4. **Session management** with automatic token refresh
5. **Authorization decorators** for protected routes

**User Management**

1. User registration and login
2. Profile management
3. Password hashing and verification
4. Session tracking

**Event Management**

1. **CRUD operations** for calendar events
2. **Date/time handling** with timezone support
3. **User-specific events** with proper isolation
4. **Event filtering** by title and date ranges
5. **Real-time updates** through the UI

**Calendar Interface**

1. **Monthly and daily views**
2. **Interactive calendar navigation**
3. **Event visualization** with color coding
4. **Responsive design** with Tailwind CSS
5. **Real-time event updates**

## 🗄️ Database Schema

### Users Table (`USERS_NUE`)
```sql
- nue_id (Primary Key)
- nue_nickname (Unique)
- nue_hashedpassword
- nue_recordcreation
- nue_recordmodification
```

### Events Table (`EVENTS_NEV`)
```sql
- nev_id (Primary Key)
- nev_title
- nev_description
- nev_starttime
- nev_endtime
- nue_nev_n_fk (Foreign Key to Users)
- nev_recordcreation
- nev_recordmodification
```

## 🔐 Security Implementation

1. **Password Security**: Bcrypt hashing with salt
2. **JWT Tokens**: Secure access/refresh token system
3. **HTTP-only Cookies**: Prevents XSS attacks
4. **CORS Configuration**: Controlled cross-origin access
5. **Input Validation**: Pydantic models for data validation
6. **SQL Injection Prevention**: SQLModel ORM protection

## 🚀 API Endpoints

### Authentication Endpoints

- `POST /api/loginJSON` - User login with JSON
- `POST /api/register` - User registration
- `POST /api/logout` - User logout
- `POST /api/refresh-token` - Token refresh
- `GET /api/me-cookie` - Get current user info

### Event Endpoints

- `GET /api/events` - Get user's events
- `POST /api/events` - Create new event
- `GET /api/events/{id}` - Get specific event
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event
- `GET /api/events/title/{title}` - Search events by title

## 🎨 Frontend Architecture

### Page Structure

- **Home Page**: Landing page with hero section
- **Login/Register**: Authentication forms
- **Diary Page**: Main calendar interface (protected)

### Component System

1. **Modular components** for reusability
2. **State management** using NiceGUI's reactive system
3. **Event-driven UI updates**
4. **Responsive design** with Tailwind CSS

### JavaScript Integration

1. **Fetch API calls** for backend communication
2. **Cookie management** for authentication
3. **Dynamic content updates**

## ⚙️ Configuration & Environment

The application uses environment variables for:

1. Database connection settings
2. JWT secret keys
3. Server port configuration
4. CORS origins
5. Cookie security settings

## 🔄 Development Workflow

### Package Management

- Uses `pip-tools` for dependency management
- `requirements.in` for direct dependencies
- `requirements.txt` for locked versions

### Development Features

1. **Hot reload** during development
2. **Automatic API documentation** via FastAPI
3. **SQL query logging** for debugging
4. **Comprehensive error handling**

## 📈 Scalability & Best Practices

1. **Separation of Concerns**: Clear layered architecture
2. **Async/Await**: Non-blocking database operations
3. **DTO Pattern**: Data validation and transformation
4. **Service Layer**: Business logic isolation
5. **Dependency Injection**: Modular and testable code
6. **Error Handling**: Comprehensive exception management

## 🎯 Key Features for Demo

1. **User Registration & Login**: Complete authentication flow
2. **Calendar Interface**: Interactive monthly/daily views
3. **Event Management**: Create, edit, delete events
4. **Real-time Updates**: Immediate UI feedback
5. **Responsive Design**: Works on different screen sizes
6. **Security**: Secure authentication with JWT cookies

This application demonstrates modern full-stack development practices using Python throughout the entire stack, showcasing how NiceGUI can be used as an alternative to traditional JavaScript frontends while maintaining a clean, scalable architecture.

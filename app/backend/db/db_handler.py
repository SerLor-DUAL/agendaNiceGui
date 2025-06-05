# app/backend/db/db_handler.py

# Import necessary modules
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from backend.config import db_settings

# Creates the asynchronous database engine
    # This engine manages the connection pool to your database in an async way.
engine:AsyncEngine = create_async_engine(
                                            db_settings.database_url,      # Database connection string from config
                                            echo= True,                 # Enable SQL query logging for debugging    
                                        )

# Creates a session factory bound to the async engine
    # This factory will generate AsyncSession instances when called.
async_session = sessionmaker(
                                bind=engine,                # Use the previously created engine       
                                expire_on_commit=False,     # Prevent objects from expiring after commit (keep them usable)
                                class_=AsyncSession         # Use async session for async DB operations
                            )

# Async function to initialize the database schema
async def init_db():
    """Initialize the database connection."""
    
    # Start a connection context with the engine
    async with engine.begin() as conn:
        print("Database connection initialized successfully.")
        
        # WARNING: Uncomment this line ONLY if you want to create the tables automatically.
            # It's unsafe to run if your database already has data because it can overwrite or cause errors.
        # await conn.run_sync(SQLModel.metadata.create_all)

# Async function that yields a database session for API routes
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session for use in routes or services."""
    
    # Open a session context with the session factory
    async with async_session() as session:
        yield session  # Yield the session so the caller can use it asynchronously
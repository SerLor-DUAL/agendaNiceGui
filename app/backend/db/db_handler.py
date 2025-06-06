# app/backend/db/db_handler.py

# Import necessary modules
from sqlmodel.ext.asyncio.session import AsyncSession                    # Importing AsyncSession for asynchronous database operations
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine      # Importing AsyncEngine and create_async_engine for creating the async engine
from sqlalchemy.orm import sessionmaker                                  # Importing sessionmaker for creating session factories
from typing import AsyncGenerator                                        # Importing AsyncGenerator for asynchronous generators
from backend.config import db_settings                                   # Importing db_settings for database settings

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Creates the asynchronous database engine, this engine manages the connection pool to your database in an async way.
engine:AsyncEngine = create_async_engine(
                                            db_settings.database_url,    # Database connection string from config
                                            echo = True,                 # Enable SQL query logging for debugging    
                                        )

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Creates a session factory bound to the async engine, this factory will generate AsyncSession instances when called.
async_session = sessionmaker(
                                bind=engine,                # Use the previously created engine       
                                expire_on_commit = False,   # Prevent objects from expiring after commit (keep them usable)
                                class_ = AsyncSession       # Use async session for async DB operations
                            )

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Async function to initialize the database schema
async def init_db():
    # Start a connection context with the engine
    async with engine.begin() as conn:
        print("Database connection initialized successfully.")
        
        # NOTE: Uncomment this line only if you want to create the tables automatically.
                # It's unsafe to run if your database already has data because it can overwrite or cause errors.
                
        # await conn.run_sync(SQLModel.metadata.create_all)

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Async function that yields a database session for API routes, it's a context manager basically
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    
    # Opens a session context with the session factory
    async with async_session() as session:
        
        # NOTE: "Yield" means the function gives back the session object temporarily, allowing the caller to use it and then resume the function after.
        yield session  

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #        
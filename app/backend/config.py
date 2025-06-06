# app/backend/config.py

# Import necessary modules
from dotenv import load_dotenv                                # Importing load_dotenv for loading environment variables
import os                                                     # Importing os for accessing environment variables

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Load environment variables from .env file
load_dotenv()

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This class handles database configuration
class DatabaseSettings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")            # Default to localhost if not set
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))              # Default to 5432 if not set (PostgreSQL default port)
    DB_NAME: str = os.getenv("DB_NAME", "postgres")             # Default to 'postgres' if not set
    DB_USER: str = os.getenv("DB_USER", "postgres")             # Default to 'postgres' if not set  
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")     # Default to 'postgres' if not set

    @property
    # Database URL for SQLModel
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This class handles user table settings
class UsersTableSettings:
    USERS_TABLE = os.getenv("DB_USERS_TABLE")
    USERS_ID_COL = os.getenv("DB_USERS_TABLE_ID")
    USERS_NICKNAME_COL = os.getenv("DB_USERS_TABLE_NICKNAME")
    USERS_HASHEDPASSWORD_COL = os.getenv("DB_USERS_TABLE_HASHEDPASSWORD")
    USERS_RECORDCREATION_COL = os.getenv("DB_USERS_TABLE_RECORDCREATION")
    USERS_RECORDMODIFICATION_COL = os.getenv("DB_USERS_TABLE_RECORDMODIFICATION")

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# NOTE: This class handles event table settings
class EventTableSettings:
    EVENTS_TABLE = os.getenv("DB_EVENTS_TABLE")
    EVENTS_ID_COL = os.getenv("DB_EVENTS_TABLE_ID")
    EVENTS_TITLE_COL = os.getenv("DB_EVENTS_TABLE_TITLE")
    EVENTS_DESCRIPTION_COL = os.getenv("DB_EVENTS_TABLE_DESCRIPTION")
    EVENTS_STARTTIME_COL = os.getenv("DB_EVENTS_TABLE_STARTTIME")
    EVENTS_ENDTIME_COL = os.getenv("DB_EVENTS_TABLE_ENDTIME")
    EVENTS_RECORDCREATION_COL = os.getenv("DB_EVENTS_TABLE_RECORDCREATION")
    EVENTS_RECORDMODIFICATION_COL = os.getenv("DB_EVENTS_TABLE_RECORDMODIFICATION")
    EVENTS_USER_ID_COL = os.getenv("DB_EVENTS_TABLE_USER_ID")

# ---------------------------------------------------------------------------------------------------------------------------------------------------- #

# Create settings instances  
db_settings = DatabaseSettings()
users_table_settings = UsersTableSettings()
events_table_settings = EventTableSettings()
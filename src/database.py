from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os


# USE FOR SEPARATELY CONNECTION WITHOUT DOCKER-COMPOSE

# dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# load_dotenv(dotenv_path)

# DB_USER = os.environ.get("POSTGRES_DB_USER")
# DB_PASSWORD = os.environ.get("POSTGRES_DB_PASSWORD")
# DB_NAME = os.environ.get("POSTGRES_DB_NAME")

# DATABASE_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@localhost:5433/{DB_NAME}" 

Base = declarative_base()

DATABASE_URI = os.environ.get("DATABASE_URI")

engine = create_async_engine(DATABASE_URI)

new_session = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)

async def get_session():
    async with new_session() as session:
          yield session
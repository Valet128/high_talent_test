from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


Base = declarative_base()

DATABASE_URL = "postgresql+asyncpg://root:1234@localhost:5431/fastapi_database"

engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(autoflush=False, autocommit=False, bind=engine)

async def get_session():
    async with new_session() as session:
          yield session
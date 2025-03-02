from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL).replace("postgresql", "postgresql+asyncpg"),
    echo=True
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[Any, Any]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
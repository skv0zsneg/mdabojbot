from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from mdabojbot.common.models import BaseModel
from mdabojbot.db import make_db_session


@pytest.fixture(scope="function")
async def db_engine():
    """Creates an in-memory SQLite database engine for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provides a transactional database session."""
    async_session = async_sessionmaker(
        db_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
def mock_db_session(db_session):
    """
    Mocks the make_db_session decorator to use the test session.
    This allows testing service functions directly with the test session.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            kwargs["session"] = db_session
            return await func(*args, **kwargs)

        return wrapper

    return decorator

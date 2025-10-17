from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from telegram.ext import Application

from mdabojbot.common.models import BaseModel

engine = create_async_engine("sqlite+aiosqlite:///mdabojbot.db", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


def make_db_session(method):
    """Decorator for easy ORM queries without session handler."""

    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper


async def init_db(application: Application):
    # TODO: Maybe change to something beautiful?
    from mdabojbot.prediction.models import Prediction  # noqa
    from mdabojbot.user.models import User  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

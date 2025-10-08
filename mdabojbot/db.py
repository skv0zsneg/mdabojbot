from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from telegram.ext import Application

from mdabojbot.common.models import BaseModel

engine = create_async_engine("sqlite+aiosqlite:///mdabojbot.db", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db(application: Application):
    # TODO: Maybe change to something beautiful?
    from mdabojbot.prediction.models import Prediction  # noqa
    from mdabojbot.rank.models import Rank, UsersRanks  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

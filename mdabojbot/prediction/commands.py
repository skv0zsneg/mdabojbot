from sqlalchemy import func, select
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from mdabojbot.db import async_session
from mdabojbot.prediction.models import Prediction


async def add_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save prediction from user."""
    if not context.args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Нафига мне пустое предсказание? Ты бы хоть одно слово написал...",
        )
        return
    prediction_text = "\n".join(context.args)

    async with async_session() as session:
        new_prediction = Prediction(telegram_user_id=update.effective_user.id, text=prediction_text)
        session.add(new_prediction)
        await session.commit()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Твоя писанина сохранена.\nМожешь собой гордится",
    )


async def what_my_future(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get random prediction for user."""
    async with async_session() as session:
        query = select(Prediction).order_by(func.random()).limit(1)
        result = await session.execute(query)
        random_prediction = result.scalar_one_or_none()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=random_prediction.text,
    )


handlers = (
    CommandHandler("add_prediction", add_prediction),
    CommandHandler("what_my_future", what_my_future),
)

import logging

from decouple import config
from telegram.ext import ApplicationBuilder

from mdabojbot import db
from mdabojbot.common.commands import handlers as common_commands
from mdabojbot.prediction.commands import handlers as prediction_commands

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_token() -> str:
    token: str = config("TELEGRAM_TOKEN")
    if token is None:
        raise ValueError("Can not get a telegram token.")
    return token


def run():
    token = get_token()
    application = ApplicationBuilder().token(token).post_init(db.init_db).build()
    application.add_handlers(
        (
            *prediction_commands,
            *common_commands,  # Always last
        )
    )
    application.run_polling()

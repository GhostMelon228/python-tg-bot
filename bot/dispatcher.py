from telegram.ext import (
    Dispatcher
)

from core.config.settings import DEBUG
from bot.main import bot


def setup_dispatcher(dp):
    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
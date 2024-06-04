from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from django.db.models import QuerySet

from core.apps.minor.models import Subject, Olympiad, Task


from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU, CALLBACK_OPEN_TASK
from bot.handlers.global_common.static_text import text_return_start, text_return_previous

from bot.handlers.presolution.manage_data import CALLBACK_SELECT_OLYMPIAD, CALLBACK_SELECT_GROUP
from bot.handlers.presolution.static_text import text_arrow_next, text_arrow_previous

def make_keyboard_for_tasks(tasks: QuerySet[Task], from_, del_, select_group, olympiad, type_grouping) -> InlineKeyboardMarkup:
    buttons = []
    arrows = []

    for task in tasks[from_:from_+del_]:
        buttons.append(
            [InlineKeyboardButton(
                text=task.title,
                callback_data=CALLBACK_OPEN_TASK.format(pk = task.id)
            )]
        )

    if from_:
        arrows.append(
            InlineKeyboardButton(
                text = text_arrow_previous,
                callback_data=CALLBACK_SELECT_GROUP.format(pk=select_group, from_ = from_ - del_)
            )
        )
    if from_ + del_ < tasks.count():
        arrows.append(
            InlineKeyboardButton(
                text = text_arrow_next,
                callback_data=CALLBACK_SELECT_GROUP.format(pk=select_group, from_ = from_ + del_)
            )
        )
    
    buttons.append(arrows)

    buttons.append(
        [InlineKeyboardButton(
            text=text_return_previous,
            callback_data=CALLBACK_SELECT_OLYMPIAD.format(pk=olympiad, sort=type_grouping)
        )]
    )

    return InlineKeyboardMarkup(buttons)
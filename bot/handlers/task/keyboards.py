from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import QuerySet

from core.apps.minor.models import Subject, Olympiad


from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU
from bot.handlers.global_common.static_text import text_return_start, text_return_previous

from bot.handlers.task.static_text import *
from bot.handlers.task.manage_data import *



def make_keyboard_for_task(queryset, task, callback, used_tip) -> InlineKeyboardMarkup:

    buttons = []

    if queryset:
        buttons.append(
            [InlineKeyboardButton(
                text=text_del_favourite_task,
                callback_data=CALLBACK_DELETE_FAVOURITE_TASK.format(pk=task)
            )]
        )
    
    else:
        buttons.append(
            [InlineKeyboardButton(
                text=text_add_favourite_task,
                callback_data=CALLBACK_CREATE_FAVOURITE_TASK.format(pk=task)
            )]
        )

    if not used_tip:
        buttons.append(
            [InlineKeyboardButton(
                text=text_add_tip,
                callback_data=CALLBACK_ADD_TIP.format(pk = task)
            )]
        )

    buttons.append(
        [InlineKeyboardButton(
            text=text_return_previous,
            callback_data=callback
        )]
    )

    return InlineKeyboardMarkup(buttons)

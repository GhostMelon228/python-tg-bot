from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.handlers.favourite_task.manage_data import *
from bot.handlers.favourite_task.static_text import *
from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU, CALLBACK_OPEN_TASK
from bot.handlers.global_common.static_text import text_return_start

def make_keyboard_for_favourite_tasks_command(tasks) -> InlineKeyboardMarkup:
    buttons = []
    for el in tasks:
        buttons.append(
            [InlineKeyboardButton(text=text_title_favourite_task.format(title=el.task.title),
                                callback_data=CALLBACK_OPEN_TASK.format(pk=el.task.pk)
            ),
            InlineKeyboardButton(text=text_delete_favourite_task, 
                                callback_data=CALLBACK_DELETE_FAVOURITE_TASK.format(pk=el.task.pk)
            )
        ])
    
    buttons.append([InlineKeyboardButton(text=text_return_start, 
                                        callback_data=CALLBACK_MAIN_MENU)
    ])

    return InlineKeyboardMarkup(buttons)
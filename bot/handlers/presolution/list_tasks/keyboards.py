from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from django.db.models import QuerySet

from core.apps.minor.models import Subject, Olympiad, Task


from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU, CALLBACK_OPEN_TASK
from bot.handlers.global_common.static_text import text_return_start, text_return_previous

from bot.handlers.presolution.manage_data import CALLBACK_TASKS_METOD, CALLBACK_SELECT_SUBJECT, CALLBACK_YEAR_SHIFT_RIGHT, CALLBACK_YEAR_SHIFT_LEFT
from bot.handlers.presolution.static_text import text_tasks_solving, text_tasks_year, text_arrow_next, text_arrow_previous, text_for_tasks

def make_keyboard_for_tasks_sorted_year_command(tasks: QuerySet[Task], subject, from_, del_, context: CallbackContext) -> InlineKeyboardMarkup:
    buttons = []

    # №1 добавление кнопок-ссылок заданий

    task_year_on_page = context.user_data["task_year"]
    new_from = from_

    for task in tasks[from_:from_+del_]:
        new_from += 1

        if task.year.number != task_year_on_page:
            context.user_data["task_year_right"] = task.year.number
            context.user_data["task_year_left"] = task.year.number
            break

        buttons.append(
            [InlineKeyboardButton(
                text=text_for_tasks.format(title=task.title),
                callback_data=CALLBACK_OPEN_TASK.format(pk=task.pk)
            )]
        )
    
    
    # №2 добавление стрелочек и кнопки, меняющей сортировку

    if from_ == 0:
        buttons.append([
            InlineKeyboardButton(text=text_tasks_solving, 
                             callback_data=CALLBACK_TASKS_METOD),
            InlineKeyboardButton(text=text_arrow_next, 
                             callback_data=CALLBACK_YEAR_SHIFT_RIGHT.format(from_=new_from))
        ])
    elif from_ + del_ >= tasks.count():
        buttons.append([
            InlineKeyboardButton(text=text_arrow_previous, 
                             callback_data=CALLBACK_YEAR_SHIFT_LEFT.format(from_=from_)),
            InlineKeyboardButton(text=text_tasks_solving, 
                             callback_data=CALLBACK_TASKS_METOD)
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text=text_arrow_previous, 
                                callback_data=CALLBACK_YEAR_SHIFT_LEFT.format(from_=from_)),
            InlineKeyboardButton(text=text_tasks_solving, 
                             callback_data=CALLBACK_TASKS_METOD),
            InlineKeyboardButton(text=text_arrow_next, 
                                callback_data=CALLBACK_YEAR_SHIFT_RIGHT.format(from_=new_from))
        ])

    # №3 добавление кнопок "Назад" и "В главное меню"

    buttons.append(
        [InlineKeyboardButton(
            text=text_return_previous,
            callback_data=CALLBACK_SELECT_SUBJECT.format(pk=subject)
        )]
    )
    buttons.append(
        [InlineKeyboardButton(
            text=text_return_start,
            callback_data=CALLBACK_MAIN_MENU
        )]
    )
    return InlineKeyboardMarkup(buttons)
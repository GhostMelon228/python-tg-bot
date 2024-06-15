from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.handlers.global_common.manage_data import CALLBACK_OPEN_TASK
from bot.handlers.global_common.static_text import text_return_previous

from bot.handlers.favourite_task.static_text import text_create_favourite_task, text_delete_favourite_task
from bot.handlers.task.static_text import *
from bot.handlers.task.manage_data import *



def make_keyboard_for_task(unnormal_answer, callback, is_favourite_task, is_used_tip) -> InlineKeyboardMarkup:

    buttons = []

    if is_favourite_task:
        buttons.append(
            [InlineKeyboardButton(
                text=text_delete_favourite_task,
                callback_data=CALLBACK_DELETE_FAVOURITE_TASK
            )]
        )
    
    else:
        buttons.append(
            [InlineKeyboardButton(
                text=text_create_favourite_task,
                callback_data=CALLBACK_CREATE_FAVOURITE_TASK
            )]
        )

    if not is_used_tip:
        buttons.append(
            [InlineKeyboardButton(
                text=text_add_tip,
                callback_data=CALLBACK_ADD_TIP
            )]
        )

    if unnormal_answer:
        buttons.append(
            [InlineKeyboardButton(
                text=text_show_solution_with_answer,
                callback_data=CALLBACK_REDIRECT_TASK_WITH_UNNNORMAL_ANSWER_TO_SOLUTION
            )]
        )

    buttons.append(
        [InlineKeyboardButton(
            text=text_return_previous,
            callback_data=callback
        )]
    )

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_right_answer(callback):

    buttons = []

    buttons.append(
        [InlineKeyboardButton(
            text=text_return_to_list_tasks,
            callback_data=callback
        )]
    )

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_wrong_answer(task, callback):
    
    buttons = []

    buttons.append(
        [InlineKeyboardButton(
            text=text_try_again,
            callback_data=CALLBACK_OPEN_TASK.format(pk=task)
        )]
    )
    buttons.append(
        [InlineKeyboardButton(
            text=text_show_solution,
            callback_data=CALLBACK_SHOW_SOLUTION
        )]
    )
    buttons.append(
        [InlineKeyboardButton(
            text=text_return_to_list_tasks,
            callback_data=callback
        )]
    )

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_solution(is_favourite_task, show_two_btns, callback):
    
    buttons = []

    if show_two_btns:
        buttons.append(
            [InlineKeyboardButton(
                text=text_ask_get_user_true_answer,
                callback_data=CALLBACK_ADD_TRUE_USER_TRY
            )]
        )
        buttons.append(
            [InlineKeyboardButton(
                text=text_ask_get_user_wrong_answer,
                callback_data=CALLBACK_ADD_WRONG_USER_TRY
            )]
        )
    
    if is_favourite_task:
        buttons.append(
            [InlineKeyboardButton(
                text=text_delete_favourite_task,
                callback_data=CALLBACK_DELETE_FAVOURITE_TASK
            )]
        )
    else:
        buttons.append(
            [InlineKeyboardButton(
                text=text_create_favourite_task,
                callback_data=CALLBACK_CREATE_FAVOURITE_TASK
            )]
        )
    buttons.append(
        [InlineKeyboardButton(
            text=text_return_to_list_tasks,
            callback_data=callback
        )]
    )

    return InlineKeyboardMarkup(buttons)
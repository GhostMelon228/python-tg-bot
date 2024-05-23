from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import QuerySet

from core.apps.minor.models import Grade

from bot.handlers.begin.manage_data import *
from bot.handlers.begin.static_text import *


def make_keyboard_for_first_start_command(grades: QuerySet[Grade]) -> InlineKeyboardMarkup:
    buttons = []
    button_start = False

    for grade in grades:

        btn = NOT_SELECTED
        callback_data = CALLBACK_CREATE_GRADE.format(pk=grade.pk)

        if grade.connection_user_to_grade.all():

            button_start = True
            btn = SELECTED
            callback_data = CALLBACK_DELETE_GRADE.format(pk=grade.pk)

        buttons.append([InlineKeyboardButton(
            text=f"{grade.title} класс {btn}", callback_data=callback_data)])

    if button_start:

        buttons.append([InlineKeyboardButton(
            text=f"Далее", callback_data=CALLBACK_START_SOLUTION)])
        

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_used_start_command() -> InlineKeyboardMarkup:
    buttons = []
    
    buttons.append([InlineKeyboardButton(
        text=start_not_created_for_favourite_button, 
        callback_data=CALLBACK_OPEN_FAVOURITE_TASKS
    )])
    
    buttons.append([InlineKeyboardButton(
        text=start_not_created_for_solution_button,
        callback_data=CALLBACK_START_SOLUTION
    )])

    return InlineKeyboardMarkup(buttons)

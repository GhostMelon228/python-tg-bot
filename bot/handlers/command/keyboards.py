from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import QuerySet

from core.apps.minor.models import Grade

from bot.handlers.command.manage_data import *
from bot.handlers.begin.static_text import *


def make_keyboard_for_change_grade(grades: QuerySet[Grade]) -> InlineKeyboardMarkup:

    buttons = []

    for grade in grades:
        buttons.append(
            [InlineKeyboardButton(
                text=f"{grade.title}" + " класс",
                callback_data=CALLBACK_CREATE_NEW_GRADE.format(pk=grade.pk)
            )]
        )
    
    return InlineKeyboardMarkup(buttons)
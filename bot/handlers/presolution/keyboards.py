from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.db.models import QuerySet

from core.apps.minor.models import Subject, Olympiad


from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU
from bot.handlers.global_common.static_text import text_return_start, text_return_previous

from bot.handlers.presolution.manage_data import *
from bot.handlers.presolution.static_text import *



def make_keyboard_for_subjects(subjects: QuerySet[Subject]) -> InlineKeyboardMarkup:
    buttons = []

    for sub in subjects:
        buttons.append(
            [InlineKeyboardButton(
                text=text_for_subject.format(title=sub.title),
                callback_data=CALLBACK_SELECT_SUBJECT.format(pk=sub.pk)
            )]
        )
    
    buttons.append(
        [InlineKeyboardButton(
            text=text_return_start,
            callback_data=CALLBACK_MAIN_MENU
        )]
    )

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_olymp_command(olympiads: QuerySet[Olympiad], subject) -> InlineKeyboardMarkup:
    buttons = []

    for olymp in olympiads:
        buttons.append(
            [InlineKeyboardButton(
                text=text_for_olympiad.format(title=olymp.title),
                callback_data=CALLBACK_SELECT_OLYMPIAD.format(pk=olymp.pk, sort="0")
            )]
        )
    
    buttons.append(
        [InlineKeyboardButton(
            text=text_return_previous,
            callback_data=CALLBACK_START_SOLVING
        )]
    )
    buttons.append(
        [InlineKeyboardButton(
            text=text_return_start,
            callback_data=CALLBACK_MAIN_MENU
        )]
    
    )
    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_groups_command(groups: QuerySet, olympiad, subject, another_sort, text_btn) -> InlineKeyboardMarkup:
    buttons = []

    for el in groups:
        if another_sort:
            title = el.number
        else:
            title = el.title
        buttons.append(
            [InlineKeyboardButton(
                text=text_for_a_criteria_group.format(title=title),
                callback_data=CALLBACK_SELECT_GROUP.format(pk=el.id, from_="0")
            )]
        )
    
    buttons.append(
        [InlineKeyboardButton(
            text=text_btn,
            callback_data=CALLBACK_SELECT_OLYMPIAD.format(pk=olympiad, sort=another_sort)
        )]
    )
    
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
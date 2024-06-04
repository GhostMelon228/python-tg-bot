from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Subject, Olympiad, Task, Year, SolveMethod

from bot.handlers.global_common.static_text import pagination_number_tasks
from bot.handlers.presolution.keyboards import *
from bot.handlers.presolution.static_text import *


def select_subject(update: Update, context: CallbackContext) -> None:

    context.user_data.pop("subject_id", None)

    user_id = extract_user_data_from_update(update)['user_id']

    context.user_data["user_id"] = user_id


    subjects = Subject.objects.filter(grades__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id))
    print(context.user_data)

    context.bot.edit_message_text(
        text=text_for_select_subjects,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_subjects(subjects)
    )

def select_olympiad(update: Update, context: CallbackContext) -> None:
    context.user_data.pop("olympiad_id", None)
    context.user_data.pop("group", None)

    user_id = extract_user_data_from_update(update)['user_id']
    subject = update.callback_query.data.split('_')[-1]

    context.user_data["subject_id"] = subject

    print(context.user_data)

    olympiads = Olympiad.objects.filter(subjects=subject, grades__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id))
    context.bot.edit_message_text(
        text=text_for_select_olympiad,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_olymp_command(olympiads, subject)
    )

def select_group(update: Update, context: CallbackContext) -> None:

    context.user_data.pop("callback_return_from_task", None)

    user_id = extract_user_data_from_update(update)['user_id']
    *args, olympiad_id, type_sort = update.callback_query.data.split('_')

    context.user_data["olympiad_id"] = olympiad_id
    context.user_data["group"] = int(type_sort)

    subject_id = context.user_data["subject_id"]


    if type_sort == "0":
        type_grouping = year_type_grouping
        tasks = Year.objects.filter(tasks__subject=subject_id, tasks__olympiad=olympiad_id).distinct()
    else:
        type_grouping = method_type_grouping
        tasks = SolveMethod.objects.filter(tasks__subject=subject_id, tasks__olympiad=olympiad_id).distinct()
    

    tasks = list(tasks)
    print(tasks)

    if type_sort == "0":  #если надо сгруппировать по Году

        text_btn = text_for_switch_to_method
        text_sort = text_years_grouping

        
    else: #если - по Методу

        text_btn = text_for_switch_to_year
        text_sort = text_method_grouping

        
    print(context.user_data)


    context.bot.edit_message_text(
        text=text_sort,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_groups_command(tasks, olympiad_id, subject_id, int(not int(type_sort)), text_btn)
    )
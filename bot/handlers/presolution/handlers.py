from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Subject, Olympiad

from bot.handlers.global_common.static_text import pagination_number_tasks
from bot.handlers.presolution.keyboards import *
from bot.handlers.presolution.static_text import *

def select_subject(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']

    subjects = Subject.objects.filter(grades__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id))
    context.user_data["user_id"] = user_id

    context.bot.edit_message_text(
        text=text_for_select_subjects,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_subjects(subjects)
    )

def select_olympiad(update: Update, context: CallbackContext) -> None:
    context.user_data.pop("olympiad_id", None)

    user_id = extract_user_data_from_update(update)['user_id']
    subject = update.callback_query.data.split('_')[-1]

    context.user_data["subject_id"] = subject
    context.user_data["del_"] = pagination_number_tasks
    context.user_data["from_"] = "0"
    context.user_data["last_from_"] = "0"

    olympiads = Olympiad.objects.filter(subjects=subject, grades__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id))
    context.bot.edit_message_text(
        text=text_for_select_olympiad,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_olymp_command(olympiads, subject)
    )
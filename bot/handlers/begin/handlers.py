from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from django.db.models import Prefetch

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.common.models import ConnectionUserGrade
from core.apps.minor.models import Grade

from bot.handlers.begin import static_text
from bot.handlers.begin.keyboards import *


def command_start(update: Update, context: CallbackContext):
    user = TelegramUser.get_user(update, context)

    user_grades = ConnectionUserGrade.objects.filter(user=user)

    context.user_data.clear()

    if not user_grades.exists():
        grades = Grade.objects.prefetch_related(Prefetch(
            "connection_user_to_grade", queryset=user_grades)).order_by('title')
        
        text = static_text.start_created.format(first_name=user.first_name)
        
        reply_markup = make_keyboard_for_first_start_command(grades)

    else:
        text = static_text.start_not_created.format(first_name=user.first_name)

        reply_markup = make_keyboard_for_used_start_command()

    update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )



def get_atr_grade(update: Update):
    user_id = extract_user_data_from_update(update)['user_id']
    grade_id = update.callback_query.data.split('_')[-1]
    grade = Grade.objects.get(id=grade_id)
    user = TelegramUser.objects.get(user_id=user_id)
    text = static_text.start_created.format(first_name=user.first_name)
    return user_id, text, user, grade


def grade_create(update: Update, context: CallbackContext) -> None:
    user_id, text, user, grade = get_atr_grade(update)

    user_grade = ConnectionUserGrade.objects.create(user=user, grade=grade)
    user_grade.save()

    text = static_text.start_created.format(first_name=user.first_name)

    grades = Grade.objects.prefetch_related(Prefetch(
        "connection_user_to_grade", queryset=ConnectionUserGrade.objects.filter(user=user))).order_by('title')

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_first_start_command(grades)
    )

def grade_delete(update: Update, context: CallbackContext) -> None:
    user_id, text, user, grade = get_atr_grade(update)

    user_grade = ConnectionUserGrade.objects.get(user=user, grade=grade)
    user_grade.delete()

    grades = Grade.objects.prefetch_related(
        Prefetch("connection_user_to_grade", 
                 queryset=ConnectionUserGrade.objects.filter(user=user)
        )
    ).order_by('title')

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_first_start_command(grades)
    )





def main_menu(update: Update, context: CallbackContext) -> None:
    user = TelegramUser.get_user(update, context)

    user_id = extract_user_data_from_update(update)['user_id']

    context.user_data.pop("subject_id", None)
    context.user_data.clear()
    

    context.bot.edit_message_text(
        text=static_text.start_not_created.format(first_name=user.first_name),
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_used_start_command()
    )
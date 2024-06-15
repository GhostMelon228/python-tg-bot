from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.common.models import ConnectionUserGrade
from core.apps.minor.models import Grade

from bot.handlers.command.keyboards import *
from bot.handlers.command.static_text import *


def change_class(update: Update, context: CallbackContext):

    grades = Grade.objects.all().order_by('title')

    update.message.reply_text(
        text=text_select_grade,
        reply_markup=make_keyboard_for_change_grade(grades)
    )

def change_grade(update: Update, context: CallbackContext):

    user_id = extract_user_data_from_update(update)['user_id']
    grade_id = update.callback_query.data.split('_')[-1]

    user = TelegramUser.get_user(update, context)
    grade = Grade.objects.get(id=grade_id)

    user_grade = ConnectionUserGrade.objects.get(user=user)
    user_grade.grade = grade
    #new_grade = ConnectionUserGrade.objects.create(user=user, grade=grade)
    user_grade.save()
    context.bot.edit_message_text(
        text=text_change_done.format(pk=grade),
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=''
    )
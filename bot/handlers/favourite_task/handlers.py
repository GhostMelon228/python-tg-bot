from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.common.models import FavouriteTasks
from core.apps.minor.models import Task

from bot.handlers.task.handlers import used_tip
from bot.handlers.task.keyboards import make_keyboard_for_task

from bot.handlers.favourite_task.keyboards import *
from bot.handlers.favourite_task.static_text import *

def open_list_favourite_tasks(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    queryset = FavouriteTasks.objects.filter(user=user_id)

    context.bot.edit_message_text(
        text=text_for_list_favourite_tasks,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_favourite_tasks_command(queryset)
    )

def favourite_task_create(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    
    task = Task.objects.get(id=update.callback_query.data.split('_')[-1])
    user = TelegramUser.objects.get(user_id=user_id)

    new_fav = FavouriteTasks.objects.create(user=user, task=task)
    new_fav.save()

    callback = context.user_data["callback_return_from_task"]
    queryset = FavouriteTasks.objects.filter(user=user, task=task)


    context.bot.edit_message_text(
        text=text_for_list_favourite_tasks,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(queryset, task.id, callback, used_tip)
    )

def favourite_task_delete(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    
    task = Task.objects.get(id=update.callback_query.data.split('_')[-1])
    user = TelegramUser.objects.get(user_id=user_id)

    new_fav = FavouriteTasks.objects.get(user=user, task=task)
    new_fav.delete()

    callback = context.user_data["callback_return_from_task"]
    queryset = FavouriteTasks.objects.filter(user=user, task=task)


    context.bot.edit_message_text(
        text=text_for_list_favourite_tasks,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(queryset, task.id, callback, used_tip)
    )
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.common.models import FavouriteTasks, UsedUserTip
from core.apps.minor.models import Task

from bot.handlers.task.keyboards import make_keyboard_for_task, make_keyboard_for_solution

from bot.handlers.favourite_task.keyboards import *
from bot.handlers.favourite_task.static_text import *


def open_list_favourite_tasks(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    context.user_data["callback_return_from_task"] = update.callback_query.data

    user = TelegramUser.objects.get(user_id=user_id)
    queryset = FavouriteTasks.objects.filter(user=user)

    context.bot.edit_message_text(
        text=text_for_list_favourite_tasks,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_favourite_tasks_command(queryset)
    )








def create_into_bd(user_id, task_id):
    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    old_fav = FavouriteTasks.objects.create(user=user, task=task)
    old_fav.save()

    return user, task



def favourite_task_create(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    
    user, task = create_into_bd(user_id, update.callback_query.data.split('_')[-1])

    is_used_tip = UsedUserTip.objects.filter(user=user, task=task).exists()

    text = task.description
    if is_used_tip:
        text += "\nПодсказка\n" + task.tip


    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(task.id, callback, True, is_used_tip)
    )


def create_for_solution_command(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    
    _, task = create_into_bd(user_id, update.callback_query.data.split('_')[-1])


    context.bot.edit_message_text(
        text="РЕШЕНИЕ:\n\n" + task.solving,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_solution(task.pk, True, callback)
    )







def delete_from_bd(user_id, task_id):
    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    old_fav = FavouriteTasks.objects.get(user=user, task=task)
    old_fav.delete()

    return user, task



def delete_favourite_task(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']

    user, _ = delete_from_bd(user_id, update.callback_query.data.split('_')[-1])
    queryset = FavouriteTasks.objects.filter(user=user)

    context.bot.edit_message_text(
        text=text_for_list_favourite_tasks,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_favourite_tasks_command(queryset)
    )


def favourite_task_delete(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    
    user, task = delete_from_bd(user_id, update.callback_query.data.split('_')[-1])

    is_used_tip = UsedUserTip.objects.filter(user=user, task=task).exists()

    text = task.description
    if is_used_tip:
        text += "\nПодсказка\n" + task.tip


    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(task.id, callback, False, is_used_tip)
    )


def delete_for_solution_command(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    
    _, task = delete_from_bd(user_id, update.callback_query.data.split('_')[-1])


    context.bot.edit_message_text(
        text="РЕШЕНИЕ:\n\n" + task.solving,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_solution(task.pk, False, callback)
    )
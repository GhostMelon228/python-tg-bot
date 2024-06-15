from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Task
from core.apps.common.models import FavouriteTasks, UserTry, UsedUserTip, UserTaskEnroll

from bot.handlers.global_common.static_text import name_answer_for_task_with_unnormal_answer
from bot.handlers.task.keyboards import *

from typing import Literal

def open_task(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    task_id = update.callback_query.data.split('_')[-1]
    context.user_data["task_id"] = task_id
    context.user_data["message_id"] = update.callback_query.message.message_id
    context.user_data["unnormal_answer"] = False


    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    if task.answer == name_answer_for_task_with_unnormal_answer:
        context.user_data["unnormal_answer"] = True

    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()
    is_used_tip = UsedUserTip.objects.filter(user=user, task=task).exists()

    new_try, _ = UserTaskEnroll.objects.get_or_create(user=user, task=task)
    new_try.status = 'PC'
    new_try.save()

    text = task.description
    print(type(text))

    if is_used_tip:
        text += "\nПодсказка\n" + task.tip
    
    if task.image_description:
        context.bot.edit_message_media(
            chat_id=user_id,
            message_id=update.callback_query.message.message_id,
            media=open(task.image_description.name, 'rb')
        )
    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(context.user_data["unnormal_answer"], callback, is_favourite_task, is_used_tip)
    )

    return 0

def add_tip(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    
    task = Task.objects.get(id=context.user_data["task_id"])
    user = TelegramUser.objects.get(user_id=user_id)

    callback = context.user_data["callback_return_from_task"]


    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()

    used_tip = UsedUserTip.objects.create(user=user, task=task)
    used_tip.save()

    text = task.description + "\nПодсказка\n" + task.tip

    if task.image_description:
        context.bot.send_photo(
            chat_id=user_id,
            photo=open(task.image_description.name, 'rb'),
            caption=text,
            reply_markup=make_keyboard_for_task(context.user_data["unnormal_answer"], callback, is_favourite_task, True)
        )
    else:
        context.bot.edit_message_text(
            text=text,
            chat_id=user_id,
            message_id=update.callback_query.message.message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=make_keyboard_for_task(context.user_data["unnormal_answer"], callback, is_favourite_task, True)
        )


def check_answer(update: Update, context: CallbackContext) -> None:

    if not context.user_data["unnormal_answer"]:
        user_id = extract_user_data_from_update(update)['user_id']

        task_id = context.user_data["task_id"]
        callback = context.user_data["callback_return_from_task"]


        task = Task.objects.get(id=task_id)
        user = TelegramUser.objects.get(user_id=user_id)

        new_state = UserTaskEnroll.objects.get(user=user, task=task)
        new_try = UserTry.objects.create(user=user, task=task)

        correct_answer = task.answer
        user_answer = update.message.text.lower()

        message_id = update.message.message_id
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=message_id)
        message_id = context.user_data["message_id"]


        if user_answer == correct_answer: #если ответ совпал

            new_state.status = 'OK'
            new_try.status = 'OK'
            new_state.save(update_fields=["status"])
            new_try.save()

            context.bot.edit_message_text(
                text=text_for_right_answer,
                chat_id=user_id,
                message_id=message_id,
                parse_mode=ParseMode.HTML,
                reply_markup=make_keyboard_for_right_answer(callback)
            )
            return ConversationHandler.END
        

        new_state.status = 'WA'
        new_try.status = 'WA'
        new_state.save(update_fields=["status"])
        new_try.save()

        context.bot.edit_message_text(
            text=text_for_wrong_answer,
            chat_id=user_id,
            message_id=message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=make_keyboard_for_wrong_answer(task_id, callback)
        )
        return 1

def show_solution(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]
    task_id = context.user_data["task_id"]


    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()
    show_2_btn = False

    if context.user_data["unnormal_answer"] and UserTaskEnroll.objects.get(user=user, task=task).status == "PC":
        show_2_btn = True

    context.bot.edit_message_text(
        text="РЕШЕНИЕ:\n\n" + task.solving,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_solution(is_favourite_task, show_2_btn, callback)
    )

def redirect_task_with_unnormal_answer(update: Update, context: CallbackContext) -> None:

    show_solution(update, context)

    return 1

def add_true_user_answer(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]
    task_id = context.user_data["task_id"]


    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()

    try_= UserTry.objects.create(user=user, task=task)
    state = UserTaskEnroll.objects.get(user=user, task=task)

    try_.status = "OK"
    state.status = "OK"
    state.save(update_fields=["status"])
    try_.save()


    context.bot.edit_message_text(
        text="РЕШЕНИЕ:\n\n" + task.solving,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_solution(is_favourite_task, False, callback)
    )

def add_wrong_user_answer(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]
    task_id = context.user_data["task_id"]


    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()

    try_, _ = UserTry.objects.get_or_create(user=user, task=task)
    state = UserTaskEnroll.objects.get(user=user, task=task)

    try_.status = "WA"
    state.status = "WA"
    state.save(update_fields=["status"])
    try_.save()

    context.bot.edit_message_text(
        text="РЕШЕНИЕ:\n\n" + task.solving,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_solution(is_favourite_task, False, callback)
    )
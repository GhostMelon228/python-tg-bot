from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Task
from core.apps.common.models import FavouriteTasks, UserAnswer, UsedUserTip

from bot.handlers.task.keyboards import *

def open_task(update: Update, context: CallbackContext) -> None:
    
    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    task_id = update.callback_query.data.split('_')[-1]
    context.user_data["task_id"] = task_id


    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()
    is_used_tip = UsedUserTip.objects.filter(user=user, task=task).exists()

    text = task.description

    if is_used_tip:
        text += "\nПодсказка\n" + task.tip

    print(context.user_data)

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(task.id, callback, is_favourite_task, is_used_tip)
    )

    return 0

def add_tip(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    
    task = Task.objects.get(id=update.callback_query.data.split('_')[-1])
    user = TelegramUser.objects.get(user_id=user_id)

    callback = context.user_data["callback_return_from_task"]


    is_favourite_task = FavouriteTasks.objects.filter(user=user, task=task).exists()

    used_tip = UsedUserTip.objects.create(user=user, task=task)
    used_tip.save()

    text = task.description + "\nПодсказка\n" + task.tip

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(task.id, callback, is_favourite_task, True)
    )

'''
def check_answer(update: Update, context: CallbackContext) -> None:
    user_answer = update.message.text.lower()
    task_id = context.user_data["task_id"]

    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    new_try = UserAnswer.objects.create(user=user, task=task, status='PC')
    new_try.save()

    correct_answer = task.answer

    message_id = update.message.message_id
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=message_id)
    message_id = context.user_data["message_id"]

    if user_answer == correct_answer:
        new_try.status = 'OK'
        new_try.save(update_fields=["status"])

        tasks, user_id, subject, olymp, from_, del_ = get_for_sorting_tasks(context)
        type_sort = int(context.user_data["type_sorting"])

        if type_sort:
            markup = make_keyboard_for_tasks_sorted_metod_command(tasks, subject, from_, del_)
        else:
            markup = make_keyboard_for_tasks_sorted_year_command(tasks, subject, from_, del_)

        context.bot.edit_message_text(
            text="Ваш ответ верен!!!!",
            chat_id=user_id,
            message_id=message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=markup
        )
        return ConversationHandler.END
    

    new_try.status = 'WA'
    new_try.save(update_fields=["status"])

    queryset, user_id, task = get_main_info_for_task(context)
    callback = "WAY_BACK"      #context.user_data["way_to_back"]

    context.bot.edit_message_text(
        text="your answer is WRONG!!!" + text_for_task,
        chat_id=user_id,
        message_id=message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(queryset, task.id, callback)
    )
    return 0
'''
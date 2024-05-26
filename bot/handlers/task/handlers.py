from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Task
from core.apps.common.models import FavouriteTasks, UserAnswer

from bot.handlers.task.keyboards import *

def open_task(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    callback = context.user_data["callback_return_from_task"]

    task_id = update.callback_query.data.split('_')[-1]
    context.user_data["task_id"] = task_id

    task = Task.objects.get(id=task_id)
    user = TelegramUser.objects.get(user_id=user_id)

    queryset = FavouriteTasks.objects.filter(user=user, task=task)

    global text_condition_task
    text_condition_task = task.description

    context.bot.edit_message_text(
        text=text_condition_task,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(queryset, task.id, callback, used_tip)
    )

def add_tip(update: Update, context: CallbackContext) -> None:

    user_id = extract_user_data_from_update(update)['user_id']
    
    task = Task.objects.get(id=update.callback_query.data.split('_')[-1])
    user = TelegramUser.objects.get(user_id=user_id)

    callback = context.user_data["callback_return_from_task"]
    queryset = FavouriteTasks.objects.filter(user=user, task=task)

    global text_condition_task, used_tip
    used_tip = True
    text_condition_task += "\n ПОДСКАЗКА: \n" + task.tip

    context.bot.edit_message_text(
        text=text_condition_task,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_task(queryset, task.id, callback, used_tip)
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
    
text_condition_task = ""
used_tip = False
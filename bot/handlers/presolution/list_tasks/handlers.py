from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Task

#from bot.handlers.global_common.static_text import pagination_number_tasks
from bot.handlers.presolution.static_text import text_for_tasks_metod, text_for_tasks_year

from bot.handlers.presolution.list_tasks.keyboards import make_keyboard_for_tasks_sorted_year_command

def universal_to_create_list_of_tasks(update: Update, context: CallbackContext):
    context_data = context.user_data
    context_data["callback_return_from_task"] = update.callback_query.data

    user_id = extract_user_data_from_update(update)['user_id']
    subject = context_data["subject_id"]
    from_ = context_data["from_"]
    del_ = context_data["del_"]

    return user_id, subject, int(from_), int(del_)

    
def list_of_tasks_by_year(update: Update, context: CallbackContext) -> None:

    olympiad = update.callback_query.data.split('_')[-1]
    context.user_data["olymp_id"] = olympiad

    user_id, subject, from_, del_ = universal_to_create_list_of_tasks(update, context)

    tasks = Task.objects.select_related("year").filter(
        subject=subject, 
        olympiad=olympiad, 
        grade__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id)
    ).order_by("-year__number")

    context.user_data.setdefault("task_year", tasks.first().year.number)

    context.bot.edit_message_text(
        text=text_for_tasks_year,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_tasks_sorted_year_command(tasks, subject, from_, del_, context)
    )



def list_of_tasks_by_metod(update: Update, context: CallbackContext) -> None:

    olympiad = context.user_data["olymp_id"]

    user_id, subject, from_, del_ = universal_to_create_list_of_tasks(update, context)

    tasks = Task.objects.select_related("solve_metod").filter(
        subject=subject, 
        olympiad=olympiad, 
        grade__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id)
    ).order_by("-solve_metod__number")


    context.bot.edit_message_text(
        text=text_for_tasks_year.format(page=int(from_ / del_) + 1),
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_tasks_sorted_year_command(tasks, subject, olympiad, context)
    )

def year_shift_right(update: Update, context: CallbackContext) -> None:

    user_id, subject, from_, del_ = universal_to_create_list_of_tasks(update, context)
    olympiad = context.user_data["olymp_id"]
    from_ = int(update.callback_query.data.split('_')[-1])

    tasks = Task.objects.select_related("year").filter(
        subject=subject, 
        olympiad=olympiad, 
        grade__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id)
    ).order_by("-year__number")

    context.user_data["task_year"] = context.user_data["task_year_right"]
    context.user_data.pop("task_year_right", None)

    context.bot.edit_message_text(
        text=text_for_tasks_year,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_tasks_sorted_year_command(tasks, subject, from_, del_, context)
    )
def year_shift_left(update: Update, context: CallbackContext) -> None:

    user_id, subject, from_, del_ = universal_to_create_list_of_tasks(update, context)
    olympiad = context.user_data["olymp_id"]
    from_ = int(update.callback_query.data.split('_')[-1])

    tasks = Task.objects.select_related("year").filter(
        subject=subject, 
        olympiad=olympiad, 
        grade__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id)
    ).order_by("-year__number")

    context.user_data["task_year"] = context.user_data["task_year_left"]
    context.user_data.pop("task_year_left", None)

    context.bot.edit_message_text(
        text=text_for_tasks_year,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_tasks_sorted_year_command(tasks, subject, from_, del_, context)
    )
from django.db.models import Prefetch

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler

from core.apps.users.models import TelegramUser, extract_user_data_from_update
from core.apps.minor.models import Task, SolveMethod, Year, Olympiad
from core.apps.common.models import UserTaskEnroll

from bot.handlers.presolution.static_text import text_for_tasks_method, text_for_tasks_year

from bot.handlers.presolution.list_tasks.keyboards import make_keyboard_for_tasks

    
def create_list_tasks(update: Update, context: CallbackContext) -> None:

    context.user_data.pop("message_id", None)
    context.user_data.pop("unnormal_answer", None)
    come_back = context.user_data.pop("task_id", 0)

    user_id = extract_user_data_from_update(update)['user_id']

    subject_id = context.user_data["subject_id"]
    olympiad_id = context.user_data["olympiad_id"]
    grouping_tasks = context.user_data["group"]

    context.user_data["callback_return_from_task"] = update.callback_query.data

    *args, select_group_id, from_ = update.callback_query.data.split('_')


    if grouping_tasks: #если выбранная группа - метод решений

        text = text_for_tasks_method.format(solve_method=SolveMethod.objects.get(id=select_group_id))

        tasks = Task.objects.select_related("solve_method").filter(
            subject=subject_id, 
            olympiad=olympiad_id,
            solve_method = int(select_group_id),
            grade__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id)
        ).prefetch_related(Prefetch("user_task_enroll", queryset=UserTaskEnroll.objects.filter(user=TelegramUser.objects.get(user_id=user_id)))).order_by("-solve_method__title")
    

    else: #если выбранная группа - год

        text = text_for_tasks_year.format(year=Year.objects.get(id=select_group_id))

        tasks = Task.objects.select_related("year").filter(
            subject=subject_id, 
            olympiad=olympiad_id,
            year = int(select_group_id),
            grade__connection_user_to_grade__user=TelegramUser.objects.get(user_id=user_id)
        ).prefetch_related(Prefetch("user_task_enroll", queryset=UserTaskEnroll.objects.filter(user=TelegramUser.objects.get(user_id=user_id)))).order_by("-year__number")


    olymp = Olympiad.objects.get(id=olympiad_id)
    print(context.user_data)


    # удаляем сообщения с заданиями и картинками

    for id in context.user_data.get("delete_messages", []):
        context.bot.delete_message(chat_id=user_id, message_id=id)
    context.user_data["delete_messages"] = []



    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML,
        reply_markup=make_keyboard_for_tasks(tasks, int(from_), olymp.tasks_in_variant, select_group_id, olympiad_id, grouping_tasks)
    )

    # если перешли через кнопку "Назад", то завершаем диалог

    if come_back:
        return ConversationHandler.END
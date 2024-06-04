from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler
)

from core.config.settings import DEBUG
from bot.main import bot


from bot.handlers.begin.handlers import command_start, grade_create, grade_delete, main_menu
from bot.handlers.favourite_task.handlers import open_list_favourite_tasks, delete_favourite_task, favourite_task_create, favourite_task_delete, create_for_solution_command, delete_for_solution_command
from bot.handlers.presolution.handlers import select_subject, select_olympiad, select_group
from bot.handlers.presolution.list_tasks.handlers import create_list_tasks
from bot.handlers.task.handlers import open_task, add_tip, check_answer, show_solution

from bot.handlers.begin.manage_data import CALLBACK_OPEN_FAVOURITE_TASKS, CALLBACK_START_SOLVING
from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", command_start))

    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(open_task, pattern=r"TASK_\d+")],
        states={
            0:[CallbackQueryHandler(add_tip, pattern=r"UNLOCK_TIP_\d+"),
               CallbackQueryHandler(favourite_task_create, pattern=r"CREATE_FAVOURITE_TASK_\d+"),
               CallbackQueryHandler(favourite_task_delete, pattern=r"DELETE_FAVOURITE_TASK_\d+"),
               MessageHandler(Filters.text & ~Filters.command, check_answer)
               ],
            1:[CallbackQueryHandler(open_task, pattern=r"TASK_\d+"),
               CallbackQueryHandler(show_solution, pattern=r"SOLUTION_FOR_TASK_\d+"),
               CallbackQueryHandler(create_for_solution_command, pattern=r"CREATE_FAVOURITE_TASK_\d+"),
               CallbackQueryHandler(delete_for_solution_command, pattern=r"DELETE_FAVOURITE_TASK_\d+")]
        },
        fallbacks=[CallbackQueryHandler(create_list_tasks, pattern=r"OBJECT_\d+_\d+"),
                   CallbackQueryHandler(open_list_favourite_tasks, pattern=CALLBACK_OPEN_FAVOURITE_TASKS)]
    ))

    dp.add_handler(CallbackQueryHandler(grade_create, pattern=r"GRADE_CREATE_\d+")) #создать класс обучения, при первом использовании бота
    dp.add_handler(CallbackQueryHandler(grade_delete, pattern=r"GRADE_DELETE_\d+")) #удалить класс обучения, при первом использовании бота

    dp.add_handler(CallbackQueryHandler(open_list_favourite_tasks, pattern=CALLBACK_OPEN_FAVOURITE_TASKS)) #вывести спиок liked задач
    dp.add_handler(CallbackQueryHandler(delete_favourite_task, pattern=r"FAVOURITE_TASK_\d+"))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern=CALLBACK_MAIN_MENU)) #вернуться в главное меню


    dp.add_handler(CallbackQueryHandler(select_subject, pattern=CALLBACK_START_SOLVING)) #выбрать предмет олимпиады
    dp.add_handler(CallbackQueryHandler(select_olympiad, pattern=r"SUBJECT_\d+")) #выбрать олимпиаду
    dp.add_handler(CallbackQueryHandler(select_group, pattern=r"OLYMPIAD_\d+_\d+")) #выбрать метод группировк
    dp.add_handler(CallbackQueryHandler(create_list_tasks, pattern=r"OBJECT_\d+_\d+")) #выбрать задание из сгрупированного списка


    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(
    bot, update_queue=None, workers=n_workers, use_context=True))

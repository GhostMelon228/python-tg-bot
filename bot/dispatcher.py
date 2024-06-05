from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, filters
)

from core.config.settings import DEBUG
from bot.main import bot


from bot.handlers.begin.handlers import command_start, grade_create, grade_delete, main_menu
from bot.handlers.command.handlers import change_grade, change_class
from bot.handlers.favourite_task.handlers import open_list_favourite_tasks, delete_favourite_task, favourite_task_create, favourite_task_delete, create_for_solution_command, delete_for_solution_command
from bot.handlers.presolution.handlers import select_subject, select_olympiad, select_group
from bot.handlers.presolution.list_tasks.handlers import create_list_tasks
from bot.handlers.task.handlers import open_task, add_tip, check_answer, show_solution, redirect_task_with_unnormal_answer

from bot.handlers.begin.manage_data import CALLBACK_OPEN_FAVOURITE_TASKS, CALLBACK_START_SOLVING
from bot.handlers.task.manage_data import CALLBACK_ADD_TIP, CALLBACK_REDIRECT_TASK_WITH_UNNNORMAL_ANSWER_TO_SOLUTION, CALLBACK_CREATE_FAVOURITE_TASK, CALLBACK_DELETE_FAVOURITE_TASK, CALLBACK_SHOW_SOLUTION
from bot.handlers.global_common.manage_data import CALLBACK_MAIN_MENU


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", command_start))

    dp.add_handler(CommandHandler("change_class", change_class))
    dp.add_handler(CallbackQueryHandler(change_grade, pattern=r"NEW_GRADE_\d+"))

    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(open_task, pattern=r"TASK_\d+")],
        states={
            0:[CallbackQueryHandler(add_tip, pattern=CALLBACK_ADD_TIP),
               CallbackQueryHandler(favourite_task_create, pattern=CALLBACK_CREATE_FAVOURITE_TASK),
               CallbackQueryHandler(favourite_task_delete, pattern=CALLBACK_DELETE_FAVOURITE_TASK),
               CallbackQueryHandler(redirect_task_with_unnormal_answer, pattern=CALLBACK_REDIRECT_TASK_WITH_UNNNORMAL_ANSWER_TO_SOLUTION),
               MessageHandler(Filters.text & ~Filters.command, check_answer)
               ],
            1:[CallbackQueryHandler(open_task, pattern=r"TASK_\d+"),
               CallbackQueryHandler(show_solution, pattern=CALLBACK_SHOW_SOLUTION),
               CallbackQueryHandler(create_for_solution_command, pattern=CALLBACK_CREATE_FAVOURITE_TASK),
               CallbackQueryHandler(delete_for_solution_command, pattern=CALLBACK_DELETE_FAVOURITE_TASK)]
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

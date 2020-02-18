import logging
import sqlite3

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

import config

# Имя файла для Базы Данных
DATABASE_NAME = "hr.db"
# Таблица, которая хранит данные о пользователях - id(айдишник в телеграме) имя, почта, профессия
USERS_TABLE = "users"
# Таблица, которая хранит данные о встречах (2 id пользователей, timestamp, когда они были сматчены и отзывы о встрече)
MEETINGS_TABLE = "meetings"

# Стандартное логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Набор состояний
START, ABOUT, RULES, FIO, EMAIL, PROFESSION, EXPERT, MODERATION, FINAL = range(9)


# Первое сообщение, которое получает пользователь, введя команду /start
def start(update, context):
    # Сценарий идет дальше, когда пользователь нажимает кнопку "Начать"
    reply_keyboard = [["Начать"]]

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот HRbazaar Random Coffee! \n \n"
             "HRbazaar Random Coffee- это проект платформы HRbazaar. "
             "Мы каждый день стараемся сделать жизнь HR-специалистов проще, лучше и интереснее. "
             "Как насчет того, чтобы немного отвлечься от рабочей рутины и познакомиться с интересным собеседником?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return START


def about(update, context):
    reply_keyboard = [["Да", "Нет"]]

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Принцип проекта максимально прост. Тебе нужно ответить на несколько вопросов о себе и выпить чашечку "
             "кофе в конце недели с классным собеседником! \n"
             "Только заранее предупреждаем: нужно быть зарегистрированным пользователем на HRbazaar. "
             "Провайдеры не допускаются к участию. \n"
             "Если оба условия совпадают, давай начинать! \n"
             "Ну что, все понятно?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return ABOUT


def fio(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Сначала напиши свое имя, фамилию и отчество."
    )
    return EMAIL


def email(update, context):
    user_id = update.effective_chat.id
    fio = update.message.text
    connection = sqlite3.connect(DATABASE_NAME)
    sql_insert = "INSERT INTO " + USERS_TABLE + "(id, name) VALUES (?, ?);"
    data_tuple = user_id, fio
    connection.execute(sql_insert, data_tuple)
    connection.commit()
    connection.close()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Мы очень рады знакомству! \n"
             "Пожалуйста, введи свой email-адрес, с помощью которого ты был зарегистрирован на HRbazaar."
    )
    return PROFESSION


def profession(update, context):
    user_id = update.effective_chat.id
    email = update.message.text
    connection = sqlite3.connect(DATABASE_NAME)
    sql_update = "UPDATE " + USERS_TABLE + " SET email = ? WHERE id = ?;"
    data_tuple = email, user_id
    connection.execute(sql_update, data_tuple)
    connection.commit()
    connection.close()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Укажи место, где ты работаешь, и свою должность. Нам будет интересно узнать, чем ты занимаешься!"
    )

    return EXPERT


def expert(update, context):
    user_id = update.effective_chat.id
    profession = update.message.text
    connection = sqlite3.connect(DATABASE_NAME)
    sql_update = "UPDATE " + USERS_TABLE + " SET profession = ? WHERE id = ?;"
    data_tuple = profession, user_id
    connection.execute(sql_update, data_tuple)
    connection.commit()
    connection.close()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Теперь расскажи нам, в чем ты разбираешься лучше всего? "
             "Укажи область своей экспертизы. Можно указать не более 3 сфер."
    )
    return FINAL


def final_step(update, context):
    user_id = update.effective_chat.id
    expert = update.message.text
    connection = sqlite3.connect(DATABASE_NAME)
    sql_update = "UPDATE " + USERS_TABLE + " SET expert = ? WHERE id = ?;"
    data_tuple = expert, user_id
    connection.execute(sql_update, data_tuple)
    connection.commit()
    connection.close()

    reply_keyboard = [["Здорово, буду ждать!"]]

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Супер! Мы уверены, что ты очень интересный собеседник! "
             "Подождешь немного, пока мы проверим твою анкету? "
             "Сразу после этого мы познакомим тебя с тем, кого ты позовешь на кофе!",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return MODERATION


def moderation(update, context):
    print('Lets wait')


def rules(update, context):
    reply_keyboard = [["Теперь понятно!"]]

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего страшного! Сейчас расскажу о правилах игры поподробнее. \n"
             "тут правила оч подробно \n"
             "Все понятно?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return FIO


def check_if_person_exist(user_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    sql_select = "SELECT * FROM " + USERS_TABLE + " WHERE id = ? LIMIT 1;"
    cursor.execute(sql_select, (user_id,))
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    if len(result) > 0:
        return True
    else:
        return False


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# Создаем таблицы в базе данных, если они еще не существуют
def create_db_tables():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("CREATE TABLE IF NOT EXISTS " + USERS_TABLE + " (id INT PRIMARY KEY NOT NULL, "
                                                                     "name TEXT,"
                                                                     "email TEXT,"
                                                                     "expert TEXT,"
                                                                     "profession TEXT);")
    connection.close()


def main():
    create_db_tables()

    # Создаем экземпляр бота используя токен. Параметр use_context используется для библиотеки выше 12 версии
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher
    # Управление командами, которые доступны пользователю
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(Filters.regex('Начать'), about)],
            ABOUT: [
                MessageHandler(Filters.regex('Да'), fio),
                MessageHandler(Filters.regex('Нет'), rules),
            ],
            FIO: [
                MessageHandler(Filters.regex('Теперь понятно'), fio),
            ],
            EMAIL: [
                MessageHandler(Filters.text, email)
            ],
            PROFESSION: [
                MessageHandler(Filters.text, profession)
            ],
            EXPERT: [
                MessageHandler(Filters.text, expert)
            ],
            FINAL: [
                MessageHandler(Filters.text, final_step)
            ],
            MODERATION: [
                MessageHandler(Filters.regex('Здорово, буду ждать!'), moderation)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conversation_handler)

    # Логируем все ошибки
    dispatcher.add_error_handler(error)

    # Запускаем бота
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
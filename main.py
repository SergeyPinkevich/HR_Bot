import logging
import config

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

# Стандартное логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Набор состояний
START, ABOUT, RULES, FIO, PROFESSION, HOBBY = range(6)


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


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Создаем экземпляр бота используя токен. Параметр use_context используется для библиотеки выше 12 версии
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher
    # Управление командами, которые доступны пользователю
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(Filters.regex('Начать'), about)],
            ABOUT: [
                MessageHandler(Filters.regex('Да'),  fio),
                MessageHandler(Filters.regex('Нет'), rules),
            ],
            FIO: [
                MessageHandler(Filters.regex('Теперь понятно'), fio),
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
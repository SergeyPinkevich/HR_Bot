from tkinter import *

import requests

import config

window = Tk()
# Ввод id пользователей, прошедших проверку
success_user_ids = Entry(window, width=60)
# Сообщение для пользователей, прошедших проверку
success_message = Entry(window, width=60)
# Ввод id пользователей, НЕ прошедших проверку
fail_user_ids = Entry(window, width=60)
# Сообщение для пользователей, НЕ прошедших проверку
fail_message = Entry(window, width=60)


def select_all(ev):
    ev.widget.select_range(0, END)


# Отправляем сообщение об успешном прохождении проверки
def send_success_message():
    success_message_text = success_message.get()
    success_user_ids_value = success_user_ids.get()
    bot_token = config.token
    send_text = 'https://api.telegram.org/bot' \
                + bot_token \
                + '/sendMessage?chat_id=' \
                + success_user_ids_value + \
                '&parse_mode=Markdown&text=' \
                + success_message_text
    response_code = requests.get(send_text).status_code
    success_user_ids.delete(0, END)
    # Если всё ок, то выводим, что сообщение дошло до пользователя
    if response_code == 200:
        success_user_ids.insert(0, "Сообщение успешно отправлено")
    # Если не удалось отправить сообщение, пишем об этом
    else:
        success_user_ids.insert(0, "Сообщение не удалось отправить")


def send_fail_message():
    fail_message_text = fail_message.get()
    fail_user_ids_value = fail_user_ids.get()
    bot_token = config.token
    send_text = 'https://api.telegram.org/bot' \
                + bot_token \
                + '/sendMessage?chat_id=' \
                + fail_user_ids_value + \
                '&parse_mode=Markdown&text=' \
                + fail_message_text
    response_code = requests.get(send_text).status_code
    fail_user_ids.delete(0, END)
    # Если всё ок, то выводим, что сообщение дошло до пользователя
    if response_code == 200:
        fail_user_ids.insert(0, "Сообщение успешно отправлено")
    # Если не удалось отправить сообщение, пишем об этом
    else:
        fail_user_ids.insert(0, "Сообщение не удалось отправить")


def main():
    window.title("HR bazaar moderation")
    window.geometry('650x600')

    success_user_ids.grid(column=0, row=0)
    success_user_ids.bind('<Command-a>', select_all)

    success_message.insert(0, "Успешно прошли модерацию")
    success_message.grid(column=0, row=1)
    success_message.bind('<Command-a>', select_all)

    success_button = Button(window, text="Отправить", command=send_success_message)
    success_button.grid(column=0, row=2, pady=20)

    fail_user_ids.grid(column=0, row=5)
    fail_user_ids.bind('<Command-a>', select_all)

    fail_message.insert(0, "Что-то пошло не так. Свяжитесь с Зиночкой")
    fail_message.grid(column=0, row=6)
    fail_message.bind('<Command-a>', select_all)

    fail_button = Button(window, text="Отправить", command=send_fail_message)
    fail_button.grid(column=0, row=7, pady=20)

    window.mainloop()


if __name__ == '__main__':
    main()

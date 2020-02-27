import sqlite3

import xlsxwriter

# Имя файла для Базы Данных
DATABASE_NAME = "hr.db"
# Таблица, которая хранит данные о пользователях - id(айдишник в телеграме) имя, почта, профессия
USERS_TABLE = "users"


def write():
    # Создаем файл, в который будем заносить данные из нашей базы
    workbook = xlsxwriter.Workbook('table.xlsx')

    # Добавляем лист в файл
    worksheet = workbook.add_worksheet()

    # Получаем данные из базы
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    sql_select = "SELECT * FROM " + USERS_TABLE
    cursor.execute(sql_select)
    result = cursor.fetchall()
    connection.commit()
    connection.close()

    # Номер строки
    row_number = 0
    # Заполняем таблицу по строчке сверху вниз из Базы Данных
    for record in result:
        # Номер столбца
        column_number = 0
        for data in record:
            try:
                worksheet.write(row_number, column_number, data)
            # Если что-то пошло не так, выводим информацию в консоль и продолжаем заполнение
            except Exception as error:
                print(error.with_traceback())
                pass
            finally:
                # Чтобы не случилось, увеличиваем счетчик для столбцов на 1
                column_number += 1
        # Заполнили все данные, переходим к следующей строке
        row_number += 1

    # Закрываем таблицу
    workbook.close()


if __name__ == '__main__':
    write()

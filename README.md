# Подготовка #

1. Проверить, что установлен Python `python3 --version
`. Должен вывести в консоль версию языка, например "Python 3.7.6". Если он не установлен, то скачать по ссылке `https://www.python.org/ftp/python/3.8.2/python-3.8.2-macosx10.9.pkg`
2. Установить библиотеки, указанные в `requirements.txt`, выполнив команду `pip install -r requirements.txt`
3. Проверить, что в репозитории есть файл `config.py`, в котором находится токен для бота

# I фаза - Сбор данных #

Запускаем файл survey.py командой `python3 survey.py`. 
По идее, он будет крутиться на удаленном сервере и беспокоиться о нем не нужно.
Задача этой фазы - собрать данные о пользователе, которые затем будут
отправлены на модерацию. 

Результатом I фазы будет База Данных `hr.db` с информацией о пользователях.

# II фаза - Модерация #

Запускаем файл excel.py командой `python3 excel.py`. Этот скрипт генериует таблицу
Excel `table.xlsx`, которую можно будет модерировать. Пользователям, прошедшим модерацию
будет отправлено сообщение об успешной проверке. Тем, кто по каким-то причинам проверку не прошел
также будет выслано сообщение в Телеграме с просьбой связаться с командой.

Отправка сообщений будет проводиться с помощью скрипта `moderation.py`, который представляет собой
простенький GUI интерфейс с возможностью ввести id пользователей, которые прошли или не прошли модерацию

# III фаза - Матчинг пользователей и сбор фидбека # 

В разработке
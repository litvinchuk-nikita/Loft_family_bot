import sqlite3
from aiogram import Bot
from datetime import timedelta, date, datetime


def now_date():
    date_1 = date.today()
    now_date = datetime.strftime(date_1, '%d.%m.%Y')
    return now_date


def now_day_month(my_date):
    my_list = my_date.split('.')
    new_date = f'{my_list[0]}.{my_list[1]}'
    return new_date


def select_all_events():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, name, date, description, price, photo FROM events')
        print("Данные получены")
        events = cur.fetchall()
        cur.close()
        event_list = []
        for event in events:
            event_list.append({'id': event[0],
                               'name': event[1],
                               'date': event[2],
                               'description': event[3],
                               'price': event[4],
                               'photo': event[5]})
        if len(event_list) != 0:
            return event_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")



def select_all_users():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, user_id, first_name, last_name, birthday, phone FROM users')
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        users_list = []
        for user in users:
            users_list.append({'id': user[0],
                              'user_id': user[1],
                              'first_name': user[2],
                              'last_name': user[3],
                              'birthday': user[4],
                              'phone': user[5]})
        if len(users_list) != 0:
            return users_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")



async def send_message_cron(bot: Bot):
    event_list = select_all_events()
    user_list = select_all_users()
    for event in event_list:
        if event['date'] == now_date():
            for user in user_list:
                try:
                    text = f'Привет, дорогой друг! Напоминаю, что сегодня проводится мероприятие "{event["name"]}", чтобы попасть к нам бесплатно, не забудь зарегестрироваться, ждем тебя :)'
                    photo = event['photo']
                    await bot.send_photo(chat_id=int(user['user_id']), photo=event['photo'], caption=text)
                except:
                    print('Произошла ошибка при отправке напоминания')
                if now_day_month(user['birthday']) == datetime.now().strftime('%d.%m'):
                    try:
                        await bot.send_message(int(user['user_id']), text=f'Порой не в силах наши поздравленья\nВ особенные, радостные дни\nРаскрыть всю глубину того значенья,\nкоторое должны нести они.\n\nНо пусть всегда светло Вам будет в жизни\nВ кругу родных, в кругу больших друзей.\nПусть много раз улыбкой счастья брызнет\nТакой же свет таких же добрых дней.\n\nС уважением LOFT FAMILY')
                    except:
                        print('Произошла ошибка при отправке напоминания')
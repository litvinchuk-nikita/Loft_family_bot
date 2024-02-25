import sqlite3
from aiogram import Bot
from datetime import timedelta, date, datetime
from keyboards.other_kb import create_question_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


def now_date():
    date_1 = date.today()
    now_date = datetime.strftime(date_1, '%d.%m.%Y')
    return now_date


def next_day_date():
    date_1 = date.today() - timedelta(days=1)
    next_day_date = datetime.strftime(date_1, '%d.%m.%Y')
    return next_day_date


def now_day_month(my_date):
    my_list = my_date.split('.')
    new_date = f'{my_list[0]}.{my_list[1]}'
    return new_date


def to_week_day_month(my_date):
    my_date = datetime.strptime(my_date, '%d.%m.%Y')
    my_date = my_date.date() - timedelta(days=7)
    my_date = datetime.strftime(my_date, '%d.%m.%Y')
    my_list = my_date.split('.')
    new_date = f'{my_list[0]}.{my_list[1]}'
    return new_date


def select_all_events():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, name, date, description, photo FROM events')
        print("Данные получены")
        events = cur.fetchall()
        cur.close()
        event_list = []
        for event in events:
            event_list.append({'id': event[0],
                               'name': event[1],
                               'date': event[2],
                               'description': event[3],
                               'photo': event[4]})
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


def select_all_registr():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, user_id, event_id FROM registr')
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        user_list = []
        for user in users:
            user_list.append({'id': user[0],
                              'user_id': user[1],
                              'event_id': user[2]})
        if len(user_list) != 0:
            return user_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_user_id_registr(event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id FROM registr WHERE event_id="%s"' % (event_id))
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        user_list = []
        for user in users:
            user_list.append(user[0])
        if len(user_list) != 0:
            return user_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_id():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id FROM ids')
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        users_list = []
        for user in users:
            users_list.append(user[0])
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


class FSMSurvey(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    question_1 = State()    # Состояние ожидания ответа на второй вопрос




async def send_message_cron(bot: Bot, state: FSMContext):
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
        if event['date'] == next_day_date():
            users_id = select_user_id_registr(event['id'])
            for user in users_id:
                bot.send_message(user, f'Вы вчера были на {event["name"]} пройдите короткий опрос, это поможет нам стать лучше :)\n\n Оцените качество музыки:', reply_markup=create_question_kb())
                await state.update_data(event_id=event['id'])
                await state.set_state(FSMSurvey.question_1)
    for user in user_list:
        if to_week_day_month(user['birthday']) == datetime.now().strftime('%d.%m'):
            try:
                await bot.send_message(int(user['user_id']), text=f'Эй! Нам тут нашептали наши агенты из службы разведки, что приближается твоё грандиозное событие и, попросили, чтобы мы подготовили для тебя подарок! Только не забудь прийти и забрать его.')
            except:
                print('Произошла ошибка при отправке поздравления 1')
        if now_day_month(user['birthday']) == datetime.now().strftime('%d.%m'):
            try:
                await bot.send_message(int(user['user_id']), text=f'Порой не в силах наши поздравленья\nВ особенные, радостные дни\nРаскрыть всю глубину того значенья,\nкоторое должны нести они.\n\nНо пусть всегда светло Вам будет в жизни\nВ кругу родных, в кругу больших друзей.\nПусть много раз улыбкой счастья брызнет\nТакой же свет таких же добрых дней.\n\nС уважением LOFT FAMILY')
            except:
                print('Произошла ошибка при отправке поздравления 2')


async def send_message_interval(bot: Bot):
    ids = select_id()
    registr_list = select_all_registr()
    registr_id_list = []
    for user in registr_list:
        registr_id_list.append(user['user_id'])
    for id in ids:
        if id not in registr_id_list:
            bot.send_message(id, f'Вы не закончили регистрацию...')
import sqlite3
from aiogram import Bot
from datetime import timedelta, date, datetime
from keyboards.other_kb import create_question_kb
from database.database import select_user, select_id, select_user_id_registr, select_all_events, select_all_users
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
    for user in user_list:
        if to_week_day_month(user['birthday']) == datetime.now().strftime('%d.%m'):
            try:
                await bot.send_message(int(user['user_id']), text=f'Эй! Нам тут нашептали наши агенты из службы разведки, что приближается твоё грандиозное событие и, попросили, чтобы мы подготовили для тебя подарок! Только не забудь прийти и забрать его.')
            except:
                print('Произошла ошибка при отправке поздравления 1')
        if now_day_month(user['birthday']) == datetime.now().strftime('%d.%m'):
            try:
                await bot.send_message(int(user['user_id']), text=f'Хэппи бёздэй и пусть хэппи будет твой эври дэй.\nЯ желаю тебе крутого настроения, постоянного драйва и движения вверх — к своим мечтам, победам, лаврам славы, звёздам желаний.\nПусть и сегодня, и через сорок лет твою пятую точку тянет в LOFT FAMILY')
            except:
                print('Произошла ошибка при отправке поздравления 2')



async def send_message_cron_2(bot: Bot):
    event_list = select_all_events()
    user_list = select_all_users()
    for event in event_list:
        if event['date'] == next_day_date():
            id_list = select_user_id_registr(event['id'])
            try:
                for id in id_list:
                    user = select_user(id)
                    await bot.send_message(chat_id=int(user['user_id']), text=f'Вы вчера были на "{event["name"]}" пройдите короткий опрос, это поможет нам стать лучше :)\n\n Оцените качество музыки:', reply_markup=create_question_kb())
            except:
                print('Произошла ошибка при отправке опроса')


async def send_message_interval(bot: Bot):
    ids = select_id()
    user_list = select_all_users()
    user_id_list = []
    for user in user_list:
        user_id_list.append(user['user_id'])
    for id in ids:
        if id not in user_id_list:
            try:
                await bot.send_message(id, f'Эээй! Надеюсь ты не из тех, кто не доводит дела до конца? 😹\n\nЗавершай скорее регистрацию и пойдем уже тусить 🕺🕺')
            except:
                print('Произошла ошибка при отправке сообщения о незаконченной регистрации')
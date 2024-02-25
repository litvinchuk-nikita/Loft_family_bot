import sqlite3



                            # функции взаимодействия с БД мероприятий (events)



def insert_event(name, date, description, photo):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO events (name, date, description, photo)'
                    ' VALUES ("%s", "%s", "%s", "%s")'
                    % (name, date, description, photo))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


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

def select_one_event(event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, name, date, description, photo FROM events WHERE id="%s"' % (event_id))
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
            return event_list[0]
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def delete_event(event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM events WHERE id="%s";' % (event_id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")




                            # функции взаимодействия с БД пользователей (users)




def insert_user(user_id, first_name, last_name, birthday, phone):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO users (user_id, first_name, last_name, birthday, phone)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s")'
                    % (user_id, first_name, last_name, birthday, phone))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def delete_user(id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM users WHERE id="%s";' % (id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
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


def select_users_id():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id FROM users')
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        users_id_list = []
        for user in users:
            users_id_list.append(user[0])
        if len(users_id_list) != 0:
            return users_id_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_one_user(user_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, user_id, first_name, last_name, birthday, phone FROM users WHERE user_id="%s"' % (user_id))
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        user_list = []
        for user in users:
            user_list.append({'id': user[0],
                              'user_id': user[1],
                              'first_name': user[2],
                              'last_name': user[3],
                              'birthday': user[4],
                              'phone': user[5]})
        if len(user_list) != 0:
            return user_list[0]
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_user(id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT user_id, first_name, last_name, birthday, phone FROM users WHERE id="%s"' % (id))
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        user_list = []
        for user in users:
            user_list.append({'user_id': user[0],
                              'first_name': user[1],
                              'last_name': user[2],
                              'birthday': user[3],
                              'phone': user[4]})
        if len(user_list) != 0:
            return user_list[0]
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")



                            # функции взаимодействия с БД регистраций на мероприятия (registr)




def insert_registr(user_id, event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO registr (user_id, event_id)'
                    ' VALUES ("%s", "%s")'
                    % (user_id, event_id))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
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


def delete_registr(id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM registr WHERE id="%s";' % (id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")




                            # функции взаимодействия с БД бронирований столиков (booking_table)




def insert_booking_table(first_name, last_name, guest, date, phone):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO booking_table (first_name, last_name, guest, date, phone)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s")'
                    % (first_name, last_name, guest, date, phone))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")



def select_booking_table(date):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT first_name, last_name, guest, phone FROM booking_table WHERE date="%s"' % (date))
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        users_list = []
        for user in users:
            users_list.append({'first_name': user[0],
                              'last_name': user[1],
                              'guest': user[2],
                              'phone': user[3]})
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







                            # функции взаимодействия с БД владельцев клубных карт (cards)




def insert_card(first_name, last_name, birthday, phone, card):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO cards (first_name, last_name, birthday, phone, card)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s")'
                    % (first_name, last_name, birthday, phone, card))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def delete_card(card):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM cards WHERE card="%s";' % (card))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_all_cards():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, first_name, last_name, birthday, phone, card FROM cards')
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        users_list = []
        for user in users:
            users_list.append({'id': user[0],
                              'first_name': user[1],
                              'last_name': user[2],
                              'birthday': user[3],
                              'phone': user[4],
                              'card': user[5]})
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


def select_cards_number():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT card FROM cards')
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        cards_list = []
        for user in users:
            cards_list.append(user[0])
        if len(cards_list) != 0:
            return cards_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_one_card(card):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, first_name, last_name, birthday, phone, card FROM cards WHERE card="%s"' % (card))
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        user_list = []
        for user in users:
            user_list.append({'id': user[0],
                              'first_name': user[1],
                              'last_name': user[2],
                              'birthday': user[3],
                              'phone': user[4],
                              'card': user[5]})
        if len(user_list) != 0:
            return user_list[0]
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")







                            # функции взаимодействия с БД опросов (survey)




def insert_survey(first_name, last_name, phone, question_1, question_2, question_3, question_4, question_5, event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO survey (first_name, last_name, phone, question_1, question_2, question_3, question_4, question_5, event_id)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
                    % (first_name, last_name, phone, question_1, question_2, question_3, question_4, question_5, event_id))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_survey(event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT first_name, last_name, phone, question_1, question_2, question_3, question_4, question_5 FROM survey WHERE event_id="%s"' % (event_id))
        print("Данные получены")
        users = cur.fetchall()
        cur.close()
        users_list = []
        for user in users:
            users_list.append({'first_name': user[0],
                              'last_name': user[1],
                              'phone': user[2],
                              'question_1': user[3],
                              'question_2': user[4],
                              'question_3': user[5],
                              'question_4': user[6],
                              'question_5': user[7]})
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









                            # функции взаимодействия с БД id всех кто использовал бота (ids)




def insert_id(user_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO ids (user_id)'
                    ' VALUES ("%s")' % (user_id))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
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






# for i in range(1, 5):
#     delete_free_table(i)
# delete_booking_table(9)
# print(f'зарегестрировано на мероприятия: {select_all_booking()}')
# # print(f'забронировано столиков: {select_all_booking_table()}')
# print(f'зарегестрировано пользователей: {select_all_users()}')
# print(select_all_events())
# delete_user(13)
# print(select_all_users())
# print(select_user_id_booking(3))
# print(select_one_user(11))
# delete_booking_table(10)
# print(select_all_booking_table())
# edit_free_place_table(5, 6)
# print(select_all_table())

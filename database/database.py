import sqlite3



                            # функции взаимодействия с БД мероприятий (events)



def insert_event(name, date, description, price, photo):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO events (name, date, description, price, photo)'
                    ' VALUES ("%s", "%s", "%s", "%s", "%s")'
                    % (name, date, description, price, photo))
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

def select_one_event(event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, name, date, description, price, photo FROM events WHERE id="%s"' % (event_id))
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

# delete_user(9)


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



                            # функции взаимодействия с БД регистраций на мероприятия (booking)




def insert_booking(user_id, event_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO booking (user_id, event_id)'
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


def select_all_booking():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, user_id, event_id FROM booking')
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


def delete_booking(id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM booking WHERE id="%s";' % (id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")




                            # функции взаимодействия с БД бронирования столиков (booking_table)




def insert_booking_table(user_id, table_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO booking_table (user_id, table_id)'
                    ' VALUES ("%s", "%s")'
                    % (user_id, table_id))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def delete_booking_table(id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('DELETE FROM booking_table WHERE id="%s";' % (id))
        conn.commit()
        print("Данные удалены")
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при обновлении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_all_booking_table():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, user_id, table_id FROM booking_table')
        print("Данные получены")
        dates = cur.fetchall()
        cur.close()
        date_list = []
        for date in dates:
            date_list.append({"id": date[0], "user_id": date[1], "table_id": date[2]})
        if len(date_list) != 0:
            return date_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")



                            # функции взаимодействия с БД наличия свободных столиков (free_table)




def insert_free_table(date, free_place):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('INSERT INTO free_table (date, free_place)'
                    ' VALUES ("%s", "%s")'
                    % (date, free_place))
        print("Данные в таблицу добавлены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_date_table():
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT date FROM free_table')
        print("Данные получены")
        dates = cur.fetchall()
        cur.close()
        date_list = []
        for date in dates:
            date_list.append(date[0])
        if len(date_list) != 0:
            return date_list
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def edit_free_place_table(new_free_place, table_id):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('UPDATE free_table SET free_place = "%s" WHERE id = "%s"' % (new_free_place, table_id))
        print("Изменения внесены")
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при добавлении данных в sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")


def select_one_table(date):
    try:
        conn = sqlite3.connect('Loft_family_bot/db.sql')
        cur = conn.cursor()
        print("База данных подключена к SQLite")
        cur.execute('SELECT id, free_place FROM free_table WHERE date = "%s"' % (date))
        print("Данные получены")
        dates = cur.fetchall()
        cur.close()
        date_list = []
        for date in dates:
            date_list.append({"id": date[0], "free_place": date[1]})
        if len(date_list) != 0:
            return date_list[0]
        else:
            return []
    except sqlite3.Error as error:
        print("Ошибка при получении данных из sqlite", error.__class__, error)
    finally:
        if (conn):
            conn.close()
            print("Соединение с SQLite закрыто")




                            # функции взаимодействия с БД владельцев клубных карт (cardss)




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



# for i in range(1, 5):
#     delete_booking(i)
# delete_booking_table(2)
# print(f'зарегестрировано на мероприятия: {select_all_booking()}')
# # print(f'забронировано столиков: {select_all_booking_table()}')
# print(f'зарегестрировано пользователей: {select_all_users()}')
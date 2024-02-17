from datetime import date, datetime, timedelta
import re

def date_func():
    date_list = []
    for i in range(7):
        now = date.today()
        date_1 = now + timedelta(days=i)
        date_1 = datetime.strftime(date_1, '%d.%m.%Y')
        date_list.append(date_1)
    return date_list


def now_time(date):
    date_1 = datetime.strptime(date, '%d.%m.%Y %H:%M')
    return date_1


def check_date(date):
    add_id = re.fullmatch(r'^[0-3][0-9]\.[0-1][0-9]\.[1-2][0-9][0-9][0-9]$', date)
    return True if add_id else False

def check_phone(phone):
    # add_id = re.fullmatch(r'^\+[7]\-\d{3}\-\d{3}-\d{2}\-\d{2}$', phone)
    add_id = re.fullmatch(r'^\d{11}$', phone)
    return True if add_id else False
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_menu_kb() -> InlineKeyboardMarkup:
    info_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Информация о нас', callback_data='info')
    registr_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Регистрация на мероприятие', callback_data='registr')
    booking_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Забронировать столик', callback_data='booking')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(info_button, registr_button, booking_button)
    kb_builder.adjust(1, 1, 1)
    return kb_builder.as_markup()


def create_date_kb(date_list) -> InlineKeyboardMarkup:
    date_1_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[0], callback_data='date_1')
    date_2_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[1], callback_data='date_2')
    date_3_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[2], callback_data='date_3')
    date_4_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[3], callback_data='date_4')
    date_5_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[4], callback_data='date_5')
    date_6_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[5], callback_data='date_6')
    date_7_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[6], callback_data='date_7')
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить бронирование', callback_data='cancel_booking')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(date_1_button, date_2_button, date_3_button, date_4_button,
                               date_5_button, date_6_button, date_7_button, cancel_button)
    kb_builder.adjust(1, 1, 1, 1, 1, 1, 1, 1)
    return kb_builder.as_markup()


def create_date_kb_2(date_list) -> InlineKeyboardMarkup:
    date_1_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[0], callback_data='date_1')
    date_2_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[1], callback_data='date_2')
    date_3_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[2], callback_data='date_3')
    date_4_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[3], callback_data='date_4')
    date_5_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[4], callback_data='date_5')
    date_6_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[5], callback_data='date_6')
    date_7_button: InlineKeyboardButton = InlineKeyboardButton(
        text=date_list[6], callback_data='date_7')
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить просмотр', callback_data='cancel_show')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(date_1_button, date_2_button, date_3_button, date_4_button,
                               date_5_button, date_6_button, date_7_button, cancel_button)
    kb_builder.adjust(1, 1, 1, 1, 1, 1, 1, 1)
    return kb_builder.as_markup()


def create_backword_menu_kb() -> InlineKeyboardMarkup:
    menu_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Вернуться в меню', callback_data='backword_menu')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(menu_button)
    return kb_builder.as_markup()


def create_yes_no_kb() -> InlineKeyboardMarkup:
    yes_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Да', callback_data='yes')
    no_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Нет', callback_data='no')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(yes_button, no_button)
    return kb_builder.as_markup()


def create_cancel_registr_kb() -> InlineKeyboardMarkup:
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить регистрацию', callback_data='cancel_registr')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(cancel_button)
    return kb_builder.as_markup()


def create_cancel_addevent_kb() -> InlineKeyboardMarkup:
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить добавление мероприятия', callback_data='cancel_addevent')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(cancel_button)
    return kb_builder.as_markup()


def create_cancel_show_kb() -> InlineKeyboardMarkup:
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить просмотр', callback_data='cancel_show')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(cancel_button)
    return kb_builder.as_markup()


def create_cancel_booking_kb() -> InlineKeyboardMarkup:
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить бронирование', callback_data='cancel_booking')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(cancel_button)
    return kb_builder.as_markup()


def create_cancel_card_kb() -> InlineKeyboardMarkup:
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить добавление карты', callback_data='cancel_card')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(cancel_button)
    return kb_builder.as_markup()



def create_cancel_newslatter_kb() -> InlineKeyboardMarkup:
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text='Отменить рассылку', callback_data='cancel_newslatter')
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.add(cancel_button)
    return kb_builder.as_markup()
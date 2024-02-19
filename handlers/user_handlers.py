from datetime import datetime, date, timedelta
# import requests
from config_data.config import Config, load_config
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType, LabeledPrice, PreCheckoutQuery
from database.database import (insert_event, select_all_events, select_one_event, delete_event, insert_user, select_all_users,
                               select_users_id, insert_booking, select_all_booking, insert_booking_table, insert_free_table,
                               select_date_table, select_one_table, edit_free_place_table, insert_card, select_all_cards, select_cards_number,
                               delete_card, select_one_card, select_one_date_table, select_user_id_booking, select_user, select_one_user,
                               select_all_booking_table)
from keyboards.other_kb import (create_menu_kb, create_date_kb, create_date_kb_2, create_backword_menu_kb, create_yes_no_kb, create_cancel_registr_kb,
                                create_cancel_addevent_kb, create_cancel_show_kb, create_cancel_booking_kb, create_cancel_card_kb, create_cancel_newslatter_kb)
from lexicon.lexicon import LEXICON
from filters.filters import IsAdmin, IsSecurity
from services.file_handling import date_func, check_date, check_phone, now_time

router: Router = Router()


# загружаем конфиг в переменную config
config: Config = load_config()



# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_cammand(message: Message, bot: Bot):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')


# этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'], reply_markup=create_backword_menu_kb(), parse_mode='HTML')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Вернуться в меню"
# и возвращать пользователя в стартовое меню
@router.callback_query(Text(text='backword_menu'), StateFilter(default_state))
async def process_backward_press(callback: CallbackQuery):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')


# этот хэндлер будет срабатывать на нажатие кнопки "информация о нас"
# и отправлять пользователю сообщение с информацией о клубе
@router.callback_query(Text(text='info'), StateFilter(default_state))
async def process_help_command(callback: CallbackQuery):
    await callback.message.delete()
    photo = URLInputFile(url=LEXICON['menu_photo'])
    text = 'ЗДЕСЬ БУДЕТ ПРИХОДИТЬ СООБЩЕНИЕ С ИНФОРМАЦИЕЙ О КЛУБЕ'
    await callback.message.answer_photo(photo=photo, caption=text,
                                  reply_markup=create_backword_menu_kb())







                                # ФУНКЦИЯ РЕГИСТРАЦИИ НА МЕРОПРИЯТИЕ









class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    event_choosing = State() # Состояние выбора мероприятия
    fill_first_name = State()   # Cостояние ввода имени
    fill_last_name = State()       # Состояние ввода фамилии
    fill_bd = State()       # Состояние ввода даты рождения
    fill_phone = State()       # Состояние ввода номера телефона
    verification_form = State() # Состояние подтверждения заполненой формы
    section_choosing = State() # Состояние выбора раздела для внесения изменений



# этот хэндлер будет срабатывать на нажатие кнопки "регистрация на мероприятие"
# и отправлять пользователю сообщение с выбором даты
@router.callback_query(Text(text='registr'), StateFilter(default_state))
async def process_help_command(callback: CallbackQuery, state: FSMContext):
    events_list = []
    id_list = []
    num = 1
    events = select_all_events()
    if len(events) != 0:
        for event in events:
            try:
                if now_time(f'{event["date"]} 22:00') < datetime.now():
                    continue
                events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                            f'Дата: {event["date"]}\n'
                            f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                id_list.append(event["id"])
            except:
                print(f"При проверке мероприятия произошла ошибка: {Exception.__class__}")
            num += 1
        if len(events_list) == 0:
            await callback.message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")
        else:
            events = f'\n\n'.join(events_list)
            text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
            await callback.message.answer(text=text, reply_markup=create_cancel_registr_kb(), parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора мероприятия
            await state.set_state(FSMFillForm.event_choosing)
            await state.update_data(id_list=id_list)
    else:
        await callback.message.answer("К сожалению на данный момент запланированных мероприятий нет, попробуйте проверить позже.")


# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMFillForm.event_choosing), lambda x: x.text.isdigit())
async def process_event_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        event = select_one_event(message.text)
        # проверяем есть ли пользователь в базе данных, если есть, автоматически заполняем форму и регистрирум
        # на мероприятие, если нету, то переходим к заполнению формы
        users = select_users_id()
        if str(message.from_user.id) in users:
            user(message.from_user.id)
            insert_booking(user['id'], event['id'])
            await message.answer_photo(photo=event['photo'], caption=f'<b>{user["first_name"]} {user["last_name"]}</b>, вы зарегестрировались на мероприятие: <b>"{event["name"]}"</b>\nДата проведения: <b>{event["date"]}</b>\n\nПокажите это сообщение на входе, чтобы пройти, до встречи :)', parse_mode='HTML')
            # Завершаем машину состояний
            await state.clear()
        else:
            # Cохраняем мероприятия в хранилище по ключу "event"
            id = event['id']
            user_id = message.from_user.id
            await state.update_data(event_id=id, user_id=user_id)
            await message.answer(text=f'Вы выбрали мероприятие: "{event["name"]}"\nВведите ваше имя', reply_markup=create_cancel_registr_kb())
            # Устанавливаем состояние ожидания ввода имени
            await state.set_state(FSMFillForm.fill_first_name)
    else:
        await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз', reply_markup=create_cancel_registr_kb())



# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.event_choosing))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Вы находитесь в процессе регистрации на мероприятие, для выбора мероприятия введите код мероприятия', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если введено корректо имя
@router.message(StateFilter(FSMFillForm.fill_first_name), lambda x: x.text.isalpha())
async def process_fill_first_name(message: Message, state: FSMContext):
    # Cохраняем имя в памяти состояния
    first_name = message.text
    await state.update_data(first_name=first_name)
    db = await state.get_data()
    if 'phone' in db.keys():
        await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
        # Устанавливаем состояние проверки анкеты
        await state.set_state(FSMFillForm.verification_form)
    else:
        await message.answer(text=f'Введите вашу фамилию', reply_markup=create_cancel_registr_kb())
        # Устанавливаем состояние ожидания ввода фамилии
        await state.set_state(FSMFillForm.fill_last_name)


# Этот хэндлер будет срабатывать, если во время
# ввода имени будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_first_name))
async def warning_fill_first_name(message: Message):
    await message.answer(
        text=f'Имя должно состоять только из букв, введите имя еще раз', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если введена корректо фамилия
@router.message(StateFilter(FSMFillForm.fill_last_name), lambda x: x.text.isalpha())
async def process_fill_last_name(message: Message, state: FSMContext):
    # Cохраняем фамилию в памяти состояния
    last_name = message.text
    await state.update_data(last_name=last_name)
    db = await state.get_data()
    if 'phone' in db.keys():
        await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
        # Устанавливаем состояние проверки анкеты
        await state.set_state(FSMFillForm.verification_form)
    else:
        await message.answer(text=f'Введите вашу дату рождения в формате dd.mm.yyyy', reply_markup=create_cancel_registr_kb())
        # Устанавливаем состояние ожидания ввода даты рождения
        await state.set_state(FSMFillForm.fill_bd)


# Этот хэндлер будет срабатывать, если во время
# ввода фамилии будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_last_name))
async def warning_fill_last_name(message: Message):
    await message.answer(
        text=f'Фамилия должна состоять только из букв, введите фамилию еще раз', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если введена корректо дата рождения
@router.message(StateFilter(FSMFillForm.fill_bd))
async def process_fill_birthday(message: Message, state: FSMContext):
    if check_date(message.text):
        # Cохраняем дату рождения в памяти состояния
        birthday = message.text
        await state.update_data(birthday=birthday)
        db = await state.get_data()
        if 'phone' in db.keys():
            await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
            # Устанавливаем состояние проверки анкеты
            await state.set_state(FSMFillForm.verification_form)
        else:
            await message.answer(text=f'Введите ваш номер телефона в формате 89997776655', reply_markup=create_cancel_registr_kb())
            # Устанавливаем состояние ожидания ввода номера телефона
            await state.set_state(FSMFillForm.fill_phone)
    else:
        await message.answer(text=f'Дата рождения должна быть в формате dd.mm.yyyy, введите дату рождения еще раз', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если во время
# ввода даты рождения будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_bd))
async def warning_fill_birthday(message: Message):
    await message.answer(text=f'Дата рождения должна быть в формате dd.mm.yyyy, введите дату рождения еще раз', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если введен корректо номер телефона
@router.message(StateFilter(FSMFillForm.fill_phone))
async def process_fill_phone(message: Message, state: FSMContext):
    if check_phone(message.text):
        # Cохраняем номер телефона в памяти состояния
        phone = message.text
        await state.update_data(phone=phone)
        db = await state.get_data()
        await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
        # Устанавливаем состояние проверки анкеты
        await state.set_state(FSMFillForm.verification_form)
    else:
        await message.answer(text=f'Номер телефона должнен быть в формате 89997776655, введите номер телефона еще раз', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если во время
# ввода номера телефона будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_phone))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Номер телефона должнен быть в формате 89997776655, введите номер телефона еще раз', reply_markup=create_cancel_registr_kb())


# этот хэндлер будет срабатывать на нажатие кнопки "да" во время проверки заполнения анкеты
# при регистрации на мероприятие и отправлать пользователю сообщение об удачной регистрации
@router.callback_query(Text(text='yes'), StateFilter(FSMFillForm.verification_form))
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    # добавляем нового пользователя в базу данных
    db = await state.get_data()
    insert_user(db['user_id'], db['first_name'], db['last_name'], db['birthday'], db['phone'])
    user = select_one_user(db['user_id'])
    # добавляем бронирование в базу данных
    insert_booking(user['id'], db['event_id'])
    event = select_one_event(db['event_id'])
    await callback.message.answer_photo(photo=event['photo'], caption=f'<b>{user["first_name"]} {user["last_name"]}</b>, вы зарегестрировались на мероприятие: <b>"{event["name"]}"</b>\nДата проведения: <b>{event["date"]}</b>\n\nПокажите это сообщение на входе, чтобы пройти, до встречи :)', parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# этот хэндлер будет срабатывать на нажатие кнопки "нет" во время проверки заполнения анкеты
# при регистрации на мероприятие и отправлать список изменений
@router.callback_query(Text(text='no'), StateFilter(FSMFillForm.verification_form))
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Выберите раздел, в который хотите внести изменения:\n1 - изменить имя;\n2 - изменить фамилию;\n3 - изменить дату рождения;\n4 - изменить номер телефона;', reply_markup=create_cancel_registr_kb())
    await state.set_state(FSMFillForm.section_choosing)


# Этот хэндлер будет срабатывать на введенный номер раздела, в котрый необходимо внести изменения
@router.message(StateFilter(FSMFillForm.section_choosing), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 4)
async def process_fill_phone(message: Message, state: FSMContext):
    db = await state.get_data()
    if int(message.text) == 1:
        await message.answer(f'Текущее имя: {db["first_name"]}\nВведите новое имя', reply_markup=create_cancel_registr_kb())
        # Устанавливаем состояние ввода имени
        await state.set_state(FSMFillForm.fill_first_name)
    elif int(message.text) == 2:
        await message.answer(f'Текущая фамилия: {db["last_name"]}\nВведите новую фамилию', reply_markup=create_cancel_registr_kb())
        # Устанавливаем состояние ввода фамилии
        await state.set_state(FSMFillForm.fill_last_name)
    elif int(message.text) == 3:
        await message.answer(f'Текущая дата рождения: {db["birthday"]}\nВведите новую дату рождения в фомате dd.mm.yyyy', reply_markup=create_cancel_registr_kb())
        # Устанавливаем состояние ввода даты рождения
        await state.set_state(FSMFillForm.fill_bd)
    elif int(message.text) == 4:
        await message.answer(f'Текущуй номер телефона: {db["phone"]}\nВведите новый номер телефона', reply_markup=create_cancel_registr_kb())
        # Устанавливаем состояние ввода номера телефона
        await state.set_state(FSMFillForm.fill_phone)


# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.section_choosing))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Для выбора раздела введите номер от 1 до 4', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать, если во время
# проверки анкеты будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.verification_form))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Для продолжения регистрации нажмите на кнопку да/нет')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить регистрацию"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_registr'), StateFilter(FSMFillForm))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Регистрация на мероприятие отменена')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()







                                    # ФУНКЦИЯ ДОБАВЛЕНИЯ МЕРОПРИЯТИЯ






class FSMAdmin(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    add_event = State()       # Состояние добавления мероприятия
    add_photo_event = State() # Состояние добаления афиши мероприятия



# Этот хэндлер будет срабатывать на отправку команды /addevent
# и отправлять в чат правила добавления мероприятия
@router.message(Command(commands='addevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addevent_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['add'], reply_markup=create_cancel_addevent_kb())
    await state.set_state(FSMAdmin.add_event)


# Этот хэндлер будет проверять правильность введенных данных
# и отправлять сообщение о добавлении фото
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.add_event))
async def process_add_event(message: Message, state: FSMContext):
    add_list = [i.strip() for i in message.text.split(';')]
    if len(add_list) == 4:
        error = 0
        if '"' in add_list[0] or "'" in add_list[0]:
            await message.answer('Нахождение ковычек в название мероприятия не допустимо, исправьте название', reply_markup=create_cancel_addevent_kb())
            error += 1
        if not check_date(add_list[1]):
            await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy', reply_markup=create_cancel_addevent_kb())
            error += 1
        if '"' in add_list[2] or "'" in add_list[2]:
            await message.answer('Нахождение ковычек в описании мероприятия не допустимо, исправьте описание', reply_markup=create_cancel_addevent_kb())
            error += 1
        if '"' in add_list[3] or "'" in add_list[3]:
            await message.answer('Нахождение ковычек в условиях входа не допустимо, исправьте условия входа', reply_markup=create_cancel_addevent_kb())
            error += 1
        if error == 0:
            await message.answer(f'Отправьте картинку c афишей в ответ на это сообщение\n', reply_markup=create_cancel_addevent_kb())
            await state.update_data(add_list=add_list)
            # Устанавливаем состояние ожидания добаления афиши
            await state.set_state(FSMAdmin.add_photo_event)
    else:
        await message.answer(f'Введенные данные о мероприятии не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте данные о мероприятии\n\n',
                             reply_markup=create_cancel_addevent_kb())


# Этот хэндлер будет добавлять мероприятие
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.add_photo_event))
async def process_add_event(message: Message, state: FSMContext):
    if message.photo:
        db = await state.get_data()
        add_list = db['add_list']
        photo = message.photo[0].file_id
        insert_event(add_list[0], add_list[1], add_list[2], add_list[3], photo)
        await message.answer('Мероприятие добавлено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n', reply_markup=create_cancel_addevent_kb())



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить добавление мероприятия"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_addevent'), StateFilter(FSMAdmin))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Добавление мероприятия отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()






                                # ФУНКЦИЯ ПРОСМОТРА РЕГИСТРАЦИИ НА МЕРОПРИЯТИЕ









class FSMShowRegistr(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    event_choosing = State() # Состояние выбора мероприятия



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить просмотр"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_show'), StateFilter(FSMShowRegistr))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Просмотр списка регистраций на мероприятие отменен')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()



# этот хэндлер будет срабатывать на команду /showregistr
# и отправлять пользователю сообщение с выбором даты
@router.message(Command(commands='showregistr'), StateFilter(default_state))
async def process_showregistr_command(message: Message, state: FSMContext):
    if message.from_user.id in config.tg_bot.admin_ids or message.from_user.id in config.tg_bot.security_ids:
        events_list = []
        id_list = []
        num = 1
        events = select_all_events()
        if len(events) != 0:
            for event in events:
                try:
                    events_list.append(f'{num}) "{event["name"]}"\n{event["description"]}\n'
                                f'Дата: {event["date"]}\n'
                                f'<b>КОД МЕРОПРИЯТИЯ 👉🏻 {event["id"]}</b>')
                    id_list.append(event["id"])
                except:
                    print(f"При проверке мероприятия произошла ошибка: {Exception.__class__}")
                num += 1
            if len(events_list) == 0:
                await message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")
            else:
                events = f'\n\n'.join(events_list)
                text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                await message.answer(text=text, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
                # Устанавливаем состояние ожидания выбора мероприятия
                await state.set_state(FSMShowRegistr.event_choosing)
                await state.update_data(id_list=id_list)
        else:
            await message.answer("К сожалению на данный момент запланированных мероприятий нет, попробуйте проверить позже.")
    else:
        await message.answer("Вы не являетесь администратором, доступ закрыт")


# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMShowRegistr.event_choosing), lambda x: x.text.isdigit())
async def process_event_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        registr_user_id = select_user_id_booking(message.text)
        event = select_one_event(message.text)
        user_list = []
        num = 1
        for id in registr_user_id:
            user = select_user(id)
            if message.from_user.id in config.tg_bot.admin_ids:
                user_list.append(f'{num}) <b>Имя</b>: {user["first_name"]}\n<b>Фамилия</b>: {user["last_name"]}\n<b>Дата рождения</b>: {user["birthday"]}\n<b>Номер телефона</b>: {user["phone"]}')
            elif message.from_user.id in config.tg_bot.security_ids:
                user_list.append(f'{num}) <b>Имя</b>: {user["first_name"]}\n<b>Фамилия</b>: {user["last_name"]}')
            num += 1
        if len(user_list) != 0:
            all_user = f'\n\n'.join(user_list)
            await message.answer(f'На {event["name"]} зарегестрировались:\n\n{all_user}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
            await state.clear()
        else:
            await message.answer(f'На {event["name"]} пока никого не зарегестрировалось', reply_markup=create_backword_menu_kb())
            await state.clear()
    else:
        await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз', reply_markup=create_cancel_show_kb())







                                    # ФУНКЦИЯ БРОНИРОВАНИЯ СТОЛИКА







class FSMBooking(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    date_choosing = State() # Состояние выбора даты
    fill_first_name = State()   # Cостояние ввода имени
    fill_last_name = State()       # Состояние ввода фамилии
    fill_bd = State()       # Состояние ввода даты рождения
    fill_phone = State()       # Состояние ввода номера телефона
    verification_form = State() # Состояние подтверждения заполненой формы
    section_choosing = State() # Состояние выбора раздела для внесения изменений
    verification_pay = State() # Состояние подтверждения оплаты


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить бронирование"
# и отменять процесс бронирования столика
@router.callback_query(Text(text='cancel_booking'), StateFilter(FSMBooking))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Бронирование отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# этот хэндлер будет срабатывать на нажатие кнопки "забронировать столик"
# и отправлять пользователю сообщение с выбором даты
@router.callback_query(Text(text='booking'))
async def process_booking_press(callback: CallbackQuery, state: FSMContext):
    date_list = date_func()
    await callback.message.delete()
    await callback.message.answer('Выберите дату, на которую хотите забронировать столик:', reply_markup=create_date_kb(date_list))
    # Устанавливаем состояние ожидания выбора даты
    await state.set_state(FSMBooking.date_choosing)




# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с датой
# во время выбора пользователя даты записи на тренировку
@router.callback_query(Text(text=['date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6', 'date_7']),
                        StateFilter(FSMBooking.date_choosing))
async def process_date_press(callback: CallbackQuery, state: FSMContext):
    date = callback.message.reply_markup.inline_keyboard[int(callback.data.split("_")[1]) - 1][0].text
    date_list = select_date_table()
    if date not in date_list:
        insert_free_table(date, 6)
    one_table = select_one_table(date)
    if int(one_table['free_place']) != 0:
        users = select_users_id()
        if str(callback.from_user.id) in users:
            await callback.message.answer_invoice(title='Бронирование столика в клубе LOFT FAMILY', description=f'Бронирование столика в клубе LOFT FAMILY с дипозитом 5000 на {date}', payload='Бронирование столика', provider_token=config.tg_bot.pay_token, currency='RUB', prices=[LabeledPrice(label='Бронирование столика', amount=500*100)])
            await state.update_data(date=date, table_id=one_table['id'], free_place=one_table['free_place'], user_id=callback.from_user.id)
            await state.set_state(FSMBooking.verification_pay)
        else:
            await callback.message.answer(f'Вы выбрали дату - {date}\n\nВведите ваше имя', reply_markup=create_cancel_booking_kb())
            await state.update_data(date=date, table_id=one_table['id'], free_place=one_table['free_place'], user_id=callback.from_user.id)
            await state.set_state(FSMBooking.fill_first_name)
    else:
        await callback.message.answer(f'На выбранную дату свободных мест не осталось, выберите дргую дату')





# Этот хэндлер будет срабатывать, если введено корректо имя
@router.message(StateFilter(FSMBooking.fill_first_name), lambda x: x.text.isalpha())
async def process_fill_first_name(message: Message, state: FSMContext):
    # Cохраняем имя в памяти состояния
    first_name = message.text
    await state.update_data(first_name=first_name)
    db = await state.get_data()
    if 'phone' in db.keys():
        await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
        # Устанавливаем состояние проверки анкеты
        await state.set_state(FSMBooking.verification_form)
    else:
        await message.answer(text=f'Введите вашу фамилию', reply_markup=create_cancel_booking_kb())
        # Устанавливаем состояние ожидания ввода фамилии
        await state.set_state(FSMBooking.fill_last_name)





# Этот хэндлер будет срабатывать, если во время
# ввода имени будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.fill_first_name))
async def warning_fill_first_name(message: Message):
    await message.answer(
        text=f'Имя должно состоять только из букв, введите имя еще раз', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать, если введена корректо фамилия
@router.message(StateFilter(FSMBooking.fill_last_name), lambda x: x.text.isalpha())
async def process_fill_last_name(message: Message, state: FSMContext):
    # Cохраняем фамилию в памяти состояния
    last_name = message.text
    await state.update_data(last_name=last_name)
    db = await state.get_data()
    if 'phone' in db.keys():
        await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
        # Устанавливаем состояние проверки анкеты
        await state.set_state(FSMBooking.verification_form)
    else:
        await message.answer(text=f'Введите вашу дату рождения в формате dd.mm.yyyy', reply_markup=create_cancel_booking_kb())
        # Устанавливаем состояние ожидания ввода даты рождения
        await state.set_state(FSMBooking.fill_bd)




# Этот хэндлер будет срабатывать, если во время
# ввода фамилии будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.fill_last_name))
async def warning_fill_last_name(message: Message):
    await message.answer(
        text=f'Фамилия должна состоять только из букв, введите фамилию еще раз', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать, если введена корректо дата рождения
@router.message(StateFilter(FSMBooking.fill_bd))
async def process_fill_birthday(message: Message, state: FSMContext):
    if check_date(message.text):
        # Cохраняем дату рождения в памяти состояния
        birthday = message.text
        await state.update_data(birthday=birthday)
        db = await state.get_data()
        if 'phone' in db.keys():
            await message.answer(text=f'Имя:{db["first_name"]}\nФамилия:{db["last_name"]}\nДата рождения:{db["birthday"]}\nНомер телефона:{db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
            # Устанавливаем состояние проверки анкеты
            await state.set_state(FSMBooking.verification_form)
        else:
            await message.answer(text=f'Введите ваш номер телефона в формате 89997776655', reply_markup=create_cancel_booking_kb())
            # Устанавливаем состояние ожидания ввода номера телефона
            await state.set_state(FSMBooking.fill_phone)
    else:
        await message.answer(text=f'Дата рождения должна быть в формате dd.mm.yyyy, введите дату рождения еще раз', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать, если во время
# ввода даты рождения будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.fill_bd))
async def warning_fill_birthday(message: Message):
    await message.answer(text=f'Дата рождения должна быть в формате dd.mm.yyyy, введите дату рождения еще раз', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать, если введен корректо номер телефона
@router.message(StateFilter(FSMBooking.fill_phone))
async def process_fill_phone(message: Message, state: FSMContext):
    if check_phone(message.text):
        # Cохраняем номер телефона в памяти состояния
        phone = message.text
        await state.update_data(phone=phone)
        db = await state.get_data()
        await message.answer(text=f'Имя: {db["first_name"]}\nФамилия: {db["last_name"]}\nДата рождения: {db["birthday"]}\nНомер телефона: {db["phone"]}\n\nВсе данные указаны верно ?', reply_markup=create_yes_no_kb())
        # Устанавливаем состояние проверки анкеты
        await state.set_state(FSMBooking.verification_form)
    else:
        await message.answer(text=f'Номер телефона должнен быть в формате 89997776655, введите номер телефона еще раз', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать, если во время
# ввода номера телефона будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.fill_phone))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Номер телефона должнен быть в формате 89997776655, введите номер телефона еще раз', reply_markup=create_cancel_booking_kb())




# этот хэндлер будет срабатывать на нажатие кнопки "да" во время проверки заполнения анкеты
# при бронировании столика и отправлать пользователю сообщение с оплатой
@router.callback_query(Text(text='yes'), StateFilter(FSMBooking.verification_form))
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    # добавляем нового пользователя в базу данных
    db = await state.get_data()
    insert_user(db['user_id'], db['first_name'], db['last_name'], db['birthday'], db['phone'])
    await callback.message.answer_invoice(title='Бронирование столика в клубе LOFT FAMILY', description=f'Бронирование столика в клубе LOFT FAMILY с дипозитом 5000 на {db["date"]}', payload='Бронирование столика', provider_token=config.tg_bot.pay_token, currency='RUB', prices=[LabeledPrice(label='Бронирование столика', amount=500*100)])
    await state.set_state(FSMBooking.verification_pay)




# этот хэндлер будет срабатывать на нажатие кнопки "нет" во время проверки заполнения анкеты
# при регистрации на мероприятие и отправлать список изменений
@router.callback_query(Text(text='no'), StateFilter(FSMBooking.verification_form))
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Выберите раздел, в который хотите внести изменения:\n1 - изменить имя;\n2 - изменить фамилию;\n3 - изменить дату рождения;\n4 - изменить номер телефона;', reply_markup=create_cancel_booking_kb())
    await state.set_state(FSMBooking.section_choosing)




# Этот хэндлер будет срабатывать на введенный номер раздела, в котрый необходимо внести изменения
@router.message(StateFilter(FSMBooking.section_choosing), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 4)
async def process_fill_phone(message: Message, state: FSMContext):
    db = await state.get_data()
    if int(message.text) == 1:
        await message.answer(f'Текущее имя: {db["first_name"]}\nВведите новое имя', reply_markup=create_cancel_booking_kb())
        # Устанавливаем состояние ввода имени
        await state.set_state(FSMBooking.fill_first_name)
    elif int(message.text) == 2:
        await message.answer(f'Текущая фамилия: {db["last_name"]}\nВведите новую фамилию', reply_markup=create_cancel_booking_kb())
        # Устанавливаем состояние ввода фамилии
        await state.set_state(FSMBooking.fill_last_name)
    elif int(message.text) == 3:
        await message.answer(f'Текущая дата рождения: {db["birthday"]}\nВведите новую дату рождения в фомате dd.mm.yyyy', reply_markup=create_cancel_booking_kb())
        # Устанавливаем состояние ввода даты рождения
        await state.set_state(FSMBooking.fill_bd)
    elif int(message.text) == 4:
        await message.answer(f'Текущуй номер телефона: {db["phone"]}\nВведите новый номер телефона', reply_markup=create_cancel_booking_kb())
        # Устанавливаем состояние ввода номера телефона
        await state.set_state(FSMBooking.fill_phone)




# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.section_choosing))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Для выбора раздела введите номер от 1 до 4', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать, если во время
# проверки анкеты будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.verification_form))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Для продолжения бронирования нажмите на кнопку да/нет', reply_markup=create_cancel_booking_kb())




# Этот хэндлер будет срабатывать на подтверждение оплаты
@router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)




# этот хэндлер будет срабатывать при успешной оплате
# и отправлять вам счет на оплату
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT, StateFilter(FSMBooking.verification_pay))
async def success(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    user = select_one_user(db['user_id'])
    insert_booking_table(user['id'], db['table_id'])
    new_free_place = int(db['free_place']) - 1
    edit_free_place_table(new_free_place, db['table_id'])
    await message.answer(f'Оплата проведена успешно👍🏻\n\n<b>{user["first_name"]} {user["last_name"]}</b> вы забронировали столик в клубе LOFT FAMILY на {db["date"]} с дипозитом на сумму 5000, ждем вас, до встречи :)', parse_mode='HTML')
    for id in config.tg_bot.admin_ids:
        await bot.send_message(id, f'<b>{user["first_name"]} {user["last_name"]}</b> забронировал(а) столик на {db["date"]}\nНомер телефона: {user["phone"]}', parse_mode='HTML')
    await state.clear()










                                # Функция просмотра бронирований столиков




class FSMShowBooking(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    date_choosing = State() # Состояние выбора даты



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить просмотр"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_show'), StateFilter(FSMShowBooking))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Просмотр списка бронирований столиков отменен')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()



# Этот хэндлер будет срабатывать на отправку команды /showbooking
# и отправлять в чат выбор даты, на которую необходимо посмотреть брони
@router.message(Command(commands='showbooking'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_showbooking_command(message: Message, state: FSMContext):
    date_list = date_func()
    await message.answer('Выбери дату, на которую хочешь посмотреть брони:', reply_markup=create_date_kb_2(date_list))
    # Устанавливаем состояние ожидания выбора даты
    await state.set_state(FSMShowBooking.date_choosing)


# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMShowBooking))
async def warning_show_booking(message: Message):
    await message.answer(text=f'Чтобы посмотреть список бронирований выберите дату или нажмити кнопку "Отменить просмотр"', reply_markup=create_cancel_show_kb())



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с датой
# во время выбора пользователя даты записи на тренировку
@router.callback_query(Text(text=['date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6', 'date_7']),
                        StateFilter(FSMShowBooking.date_choosing))
async def process_date_press(callback: CallbackQuery, state: FSMContext):
    date = callback.message.reply_markup.inline_keyboard[int(callback.data.split("_")[1]) - 1][0].text
    booking = select_all_booking_table()
    booking_list = []
    num = 1
    for book in booking:
        user = select_user(book['user_id'])
        date_table = select_one_date_table(book['table_id'])
        if date == date_table:
            booking_list.append(f'{num}) Имя: {user["first_name"]}\nФамилия: {user["last_name"]}\nДата рождения: {user["birthday"]}\nНомер телефона: {user["phone"]}')
            num += 1
    if len(booking_list) != 0:
        all_booking = f'\n\n'.join(booking_list)
        await callback.message.answer(f'На {date} забронировали столики:\n\n{all_booking}', reply_markup=create_backword_menu_kb())
        await state.clear()
    else:
        await callback.message.answer(f'На {date} столики не бронировали', reply_markup=create_backword_menu_kb())
        await state.clear()





                                 # Функция добавления владельцев клубных карт






class FSMCard(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    add_card = State()       # Состояние добавления карты
    # show_card = State()     # Состояние просмотра всех карт


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить добавление карты"
# и отменять процесс бронирования столика
@router.callback_query(Text(text='cancel_card'), StateFilter(FSMCard))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Добавление карты отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать на отправку команды /addcard
# и отправлять в чат правила добавления карты
@router.message(Command(commands='addcard'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addcard_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['addcard'], reply_markup=create_cancel_card_kb())
    await state.set_state(FSMCard.add_card)







# Этот хэндлер будет проверять правильность введенных данных
# и отправлять сообщение о необходим изменениях или добавлять владельца карты
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMCard.add_card))
async def process_add_event(message: Message, state: FSMContext):
    add_list = [i.strip() for i in message.text.split(';')]
    if len(add_list) == 5:
        error = 0
        if not add_list[0].isalpha():
            await message.answer('Имя должно состоять только из букв, исправьте имя', reply_markup=create_cancel_card_kb())
            error += 1
        if not add_list[1].isalpha():
            await message.answer('Фамилия должна состоять только из букв, исправьте фамилию', reply_markup=create_cancel_card_kb())
            error += 1
        if not check_date(add_list[2]):
            await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy', reply_markup=create_cancel_card_kb())
            error += 1
        if not check_phone(add_list[3]):
            await message.answer(f'Номер телефона введен не в верном формате, введите номер телефона в формате:\n89997776655', reply_markup=create_cancel_card_kb())
            error += 1
        if not add_list[4].isdigit():
            await message.answer('Номер карты должен быть числом, исправьте номер карты', reply_markup=create_cancel_card_kb())
            error += 1
        cards = select_cards_number()
        if add_list[4] in cards:
            await message.answer('Пользователь с таким номером карты уже добавлен, исправьте номер карты', reply_markup=create_cancel_card_kb())
            error += 1
        if error == 0:
            insert_card(add_list[0], add_list[1], add_list[2], add_list[3], add_list[4])
            await message.answer('Владелец клубной карты добавлен', reply_markup=create_backword_menu_kb())
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Введенные данные не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте их еще раз', reply_markup=create_cancel_card_kb())







                                 # Функция просмотра владельцев клубных карт





# Этот хэндлер будет срабатывать на отправку команды /showcard
# и отправлять в чат список со всеми владельцами карт
@router.message(Command(commands='showcard'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addcard_command(message: Message, state: FSMContext):
    card_list = []
    cards = select_all_cards()
    num = 1
    for card in cards:
        card_list.append(f'{num}) Номер клубной карты: {card["card"]}\nИмя: {card["first_name"]}\nФамилия: {card["last_name"]}\nДата рождения: {card["birthday"]}\nНомер телефона: {card["phone"]}')
        num += 1
    all_card = f'\n\n'.join(card_list)
    await message.answer(f'{all_card}', reply_markup=create_backword_menu_kb())








                                 # Функция рассылки афиши







class FSMNewsletter(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    create_text = State()    # Состояние создания текста рассылки
    add_photo = State()     # Состояние добавления фото
    verification_newslatter = State() # Состояние подтверждения рассылки


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить рассылку"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_newslatter'), StateFilter(FSMNewsletter))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    text = f"{LEXICON['/start']}"
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Рассылка отменена')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать на отправку команды /sendnewsletter
# и отправлять в чат доступные для рассылки мероприятия
@router.message(IsAdmin(config.tg_bot.admin_ids), Command(commands='sendnewsletter'), StateFilter(default_state))
async def process_sendnewsletter_command(message: Message, state: FSMContext):
    await message.answer('Введите текст рассылки', reply_markup=create_cancel_newslatter_kb())
    await state.set_state(FSMNewsletter.create_text)


# Этот хэндлер будет сохранять текст рассылки и отправлять сообщение о добавлении фото
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.create_text))
async def process_create_text_newsletter(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    db = await state.get_data()
    if 'photo' in db.keys():
        await message.answer(f'Ниже представлена сформированная рассылка, введите:\n\n1 - чтобы отправить текущий вариант;\n2 - чтобы изменить текст;\n3 - чтобы изменить фото', reply_markup=create_cancel_newslatter_kb())
        await message.answer_photo(photo=db['photo'], caption=db['text'])
        # Устанавливаем состояние ожидания подтверждения сформированной рассылки
        await state.set_state(FSMNewsletter.verification_newslatter)
    else:
        await message.answer('Добавьте фото рассылки', reply_markup=create_cancel_newslatter_kb())
        # Устанавливаем состояние ожидания добавления фото
        await state.set_state(FSMNewsletter.add_photo)



# Этот хэндлер отправлять сообщение с готовой рассылкой и правилами подтверждения отправки/изменения
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMNewsletter.add_photo))
async def process_create_text_newsletter(message: Message, state: FSMContext):
    if message.photo:
        db = await state.get_data()
        photo = message.photo[0].file_id
        await message.answer(f'Ниже представлена сформированная рассылка, введите:\n\n1 - чтобы отправить текущий вариант;\n2 - чтобы изменить текст;\n3 - чтобы изменить фото', reply_markup=create_cancel_newslatter_kb())
        await message.answer_photo(photo=photo, caption=db['text'])
        await state.update_data(photo=photo)
        # Устанавливаем состояние ожидания подтверждения сформированной рассылки
        await state.set_state(FSMNewsletter.verification_newslatter)
    else:
        await message.answer('Добавьте фото рассылки', reply_markup=create_cancel_newslatter_kb())



# Этот хэндлер будет срабатывать на введенный номер раздела при подтверждении рассылки
@router.message(StateFilter(FSMNewsletter.verification_newslatter), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 3)
async def process_fill_phone(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    if int(message.text) == 1:
        db = await state.get_data()
        users_id = select_users_id()
        for id in users_id:
            try:
                await bot.send_photo(chat_id=id, photo=db['photo'], caption=db['text'])
            except:
                print(f'Произошла ошибка при отправке рассылки на id - {id}')
        await message.answer('Рассылка отправлена', reply_markup=create_backword_menu_kb())
        await state.clear()
    elif int(message.text) == 2:
        await message.answer(f'Введите новый текст рассылки', reply_markup=create_cancel_newslatter_kb())
        # Устанавливаем состояние ввода текста рассылки
        await state.set_state(FSMNewsletter.create_text)
    elif int(message.text) == 3:
        await message.answer(f'Отправьте новое фото рассылки', reply_markup=create_cancel_newslatter_kb())
        # Устанавливаем состояние добавления фото
        await state.set_state(FSMNewsletter.add_photo)


# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMNewsletter.verification_newslatter))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Для выбора раздела введите номер от 1 до 3', reply_markup=create_cancel_newslatter_kb())
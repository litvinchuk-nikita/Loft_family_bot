from datetime import datetime, date, timedelta
import time
from config_data.config import Config, load_config
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message, URLInputFile, InputMediaPhoto, ContentType
from database.database import (insert_event, select_all_events, select_one_event, delete_event, insert_user, select_all_users,
                               select_users_id, insert_registr, select_all_registr, insert_card, select_all_cards, select_cards_number,
                               delete_card, select_one_card, select_user_id_registr, select_user, select_one_user, insert_booking_table,
                               select_booking_table, select_survey, insert_survey, insert_id, select_id, select_all_ids, select_one_event_id)
from keyboards.other_kb import (create_menu_kb, create_date_kb, create_date_kb_2, create_backword_menu_kb,          create_yes_no_kb, create_cancel_registr_kb,
                                create_cancel_addevent_kb, create_cancel_show_kb, create_cancel_booking_kb, create_cancel_card_kb, create_cancel_newslatter_kb,
                                create_question_kb, create_question_2_kb, create_question_3_kb, create_cancel_addbooking_kb, create_cancel_delete_card_kb,
                                create_cancel_deleteevent_kb, create_cancel_survey_kb)
from lexicon.lexicon import LEXICON
from filters.filters import IsAdmin, IsSecurity
from services.file_handling import date_func, check_date, check_phone, now_time, next_day_date, next_day_date_2

router: Router = Router()


# загружаем конфиг в переменную config
config: Config = load_config()



# этот хэндлер будет срабатывать на команду "/start" -
# и отправлять ему стартовое меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_cammand(message: Message, bot: Bot):
    ids_list = select_id()
    if str(message.from_user.id) not in ids_list:
        insert_id(message.from_user.id)
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')


# этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    if message.from_user.id in config.tg_bot.admin_ids:
        await message.answer(LEXICON['/help_admin'], reply_markup=create_backword_menu_kb(), parse_mode='HTML')
    elif message.from_user.id in config.tg_bot.security_ids:
        await message.answer(LEXICON['/help_security'], reply_markup=create_backword_menu_kb(), parse_mode='HTML')
    else:
        await message.answer(LEXICON['/help'], reply_markup=create_backword_menu_kb(), parse_mode='HTML')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Вернуться в меню"
# и возвращать пользователя в стартовое меню
@router.callback_query(Text(text='backword_menu'), StateFilter(default_state))
async def process_backward_press(callback: CallbackQuery):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')


# этот хэндлер будет срабатывать на нажатие кнопки "информация о нас"
# и отправлять пользователю сообщение с информацией о клубе
@router.callback_query(Text(text='info'), StateFilter(default_state))
async def process_help_command(callback: CallbackQuery):
    await callback.message.delete()
    photo = URLInputFile(url=LEXICON['menu_photo'])
    text = LEXICON['info']
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
            user = select_one_user(message.from_user.id)
            insert_registr(user['id'], event['id'])
            await message.answer_photo(photo=event['photo'], caption=f'<b>{user["first_name"]} {user["last_name"]}</b>, вы зарегестрировались на мероприятие: <b>"{event["name"]}"</b>\nДата проведения: <b>{event["date"]}</b>\n\nПокажите это сообщение на входе, чтобы пройти, до встречи :)', parse_mode='HTML')
            # Завершаем машину состояний
            await state.clear()
        else:
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
    insert_registr(user['id'], db['event_id'])
    event = select_one_event(db['event_id'])
    await callback.message.delete()
    await callback.message.answer_photo(photo=event['photo'], caption=f'<b>{user["first_name"]} {user["last_name"]}</b>, вы зарегестрировались на мероприятие: <b>"{event["name"]}"</b>\nДата проведения: <b>{event["date"]}</b>\n\nПокажите это сообщение на входе, чтобы пройти, до встречи :)', parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# этот хэндлер будет срабатывать на нажатие кнопки "нет" во время проверки заполнения анкеты
# при регистрации на мероприятие и отправлать список изменений
@router.callback_query(Text(text='no'), StateFilter(FSMFillForm.verification_form))
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
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
    await message.answer(text=f'Для продолжения регистрации нажмите на кнопку да/нет', reply_markup=create_cancel_registr_kb())


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить регистрацию"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_registr'), StateFilter(FSMFillForm))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Регистрация на мероприятие отменена')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
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
    delete_event = State()    # Состояние удаления мероприятия



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
    if len(add_list) == 3:
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
        if error == 0:
            await message.answer(f'Добавьте афишу мероприятия\n', reply_markup=create_cancel_addevent_kb())
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
        insert_event(add_list[0], add_list[1], add_list[2], photo)
        await message.answer('Мероприятие добавлено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(f'Отправленное сообщение не является картинкой, отправте картинку афиши\n', reply_markup=create_cancel_addevent_kb())



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить добавление мероприятия"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_addevent'), StateFilter(FSMAdmin))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Добавление мероприятия отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()







                                # Функция удаления мероприятия






# Этот хэндлер будет срабатывать на отправку команды /deleteevent
# и отправлять в чат правила добавления мероприятия
@router.message(Command(commands='deleteevent'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addevent_command(message: Message, state: FSMContext):
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
            await message.answer("К сожалению на данный момент нету запланированных мероприятий, попробуйте проверить позже.")
        else:
            events = f'\n\n'.join(events_list)
            text = f"{events}\n\n<i>ЧТОБЫ УДАЛИТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
            await message.answer(text=text, reply_markup=create_cancel_deleteevent_kb(), parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора мероприятия
            await state.set_state(FSMAdmin.delete_event)
            await state.update_data(id_list=id_list)
    else:
        await message.answer("К сожалению на данный момент запланированных мероприятий нет, попробуйте проверить позже.")


# Этот хэндлер будет проверять правильность введенных данных
# и отправлять сообщение о добавлении фото
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMAdmin.delete_event), lambda x: x.text.isdigit())
async def process_delete_event(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    if int(message.text) in id_list:
        delete_event(int(message.text))
        await message.answer('Мероприятие удалено')
        # Завершаем машину состояний
        await state.clear()
    else:
        await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз', reply_markup=create_cancel_deleteevent_kb())



# Этот хэндлер будет срабатывать, если во время
# выбора мероприятия будет введено что-то некорректное
@router.message(StateFilter(FSMAdmin.delete_event))
async def warning_not_event(message: Message):
    await message.answer(
        text=f'Для удаления мероприятия введите код мероприятия', reply_markup=create_cancel_deleteevent_kb())




# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить удаление мероприятия"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_deleteevent'), StateFilter(FSMAdmin))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Удаление мероприятия отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()










                                # ФУНКЦИЯ ПРОСМОТРА ВСЕХ ЗАРЕГИСТРИРОВАННЫХ



# этот хэндлер будет срабатывать на команду /show_all_registr
# и отправлять пользователю сообщение с выбором даты
@router.message(Command(commands='show_all_registr'), StateFilter(default_state))
async def process_show_all_registr_command(message: Message):
    if message.from_user.id in config.tg_bot.admin_ids:
        all_registr = select_all_users()
        user_list = []
        num = 1
        for user in all_registr:
            user_list.append(f'{num}) <b>Имя</b>: {user["first_name"]}\n<b>Фамилия</b>: {user["last_name"]}\n<b>Дата рождения</b>: {user["birthday"]}\n<b>Номер телефона</b>: {user["phone"]}')
            num += 1
        num_1 = 1
        for user in user_list:
            await message.answer(text=user, parse_mode='HTML')
            num_1 += 1
            if num_1 % 50 == 0:
                time.sleep(6)




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
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Просмотр списка регистраций на мероприятие отменен')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
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
                    if next_day_date() >= now_time(f'{event["date"]} 00:00'):
                        continue
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
                if len(events_list) <= 20:
                    events = f'\n\n'.join(events_list)
                    text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                    await message.answer(text=text, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
                elif len(events_list) >= 21 and len(events_list) <= 40:
                    events_1 = f'\n\n'.join(events_list[0:20])
                    events_2 = f'\n\n'.join(events_list[20:])
                    text_1 = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events_1}"
                    text_2 = f"{events_2}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                    await message.answer(text=text_1,parse_mode='HTML')
                    await message.answer(text=text_2, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
                elif len(events_list) >= 41 and len(events_list) <= 60:
                    events_1 = f'\n\n'.join(events_list[0:20])
                    events_2 = f'\n\n'.join(events_list[20:40])
                    events_3 = f'\n\n'.join(events_list[40:])
                    text_1 = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events_1}"
                    text_2 = f"{events_2}"
                    text_3 = f"{events_3}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                    await message.answer(text=text_1, parse_mode='HTML')
                    await message.answer(text=text_2, parse_mode='HTML')
                    await message.answer(text=text_3, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
                elif len(events_list) >= 61 and len(events_list) <= 80:
                    events_1 = f'\n\n'.join(events_list[0:20])
                    events_2 = f'\n\n'.join(events_list[20:40])
                    events_3 = f'\n\n'.join(events_list[40:60])
                    events_4 = f'\n\n'.join(events_list[60:])
                    text_1 = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events_1}"
                    text_2 = f"{events_2}"
                    text_3 = f"{events_3}"
                    text_4 = f"{events_4}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                    await message.answer(text=text_1, parse_mode='HTML')
                    await message.answer(text=text_2, parse_mode='HTML')
                    await message.answer(text=text_3, parse_mode='HTML')
                    await message.answer(text=text_4, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
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
        registr_user_id = select_user_id_registr(message.text)
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
            if len(user_list) <= 30:
                all_user = f'\n\n'.join(user_list)
                await message.answer(f'На {event["name"]} зарегестрировались:\n\n{all_user}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
            elif len(user_list) >= 31 and len(user_list) <= 60:
                all_user_1 = f'\n\n'.join(user_list[0:30])
                all_user_2 = f'\n\n'.join(user_list[30:])
                await message.answer(f'На {event["name"]} зарегестрировались:\n\n{all_user_1}', parse_mode='HTML')
                await message.answer(f'{all_user_2}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
            elif len(user_list) >= 61 and len(user_list) <= 90:
                all_user_1 = f'\n\n'.join(user_list[0:30])
                all_user_2 = f'\n\n'.join(user_list[30:60])
                all_user_3 = f'\n\n'.join(user_list[60:])
                await message.answer(f'На {event["name"]} зарегестрировались:\n\n{all_user_1}', parse_mode='HTML')
                await message.answer(f'{all_user_2}', parse_mode='HTML')
                await message.answer(f'{all_user_3}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
            elif len(user_list) >= 91 and len(user_list) <= 120:
                all_user_1 = f'\n\n'.join(user_list[0:30])
                all_user_2 = f'\n\n'.join(user_list[30:60])
                all_user_3 = f'\n\n'.join(user_list[60:90])
                all_user_4 = f'\n\n'.join(user_list[90:])
                await message.answer(f'На {event["name"]} зарегестрировались:\n\n{all_user_1}', parse_mode='HTML')
                await message.answer(f'{all_user_2}', parse_mode='HTML')
                await message.answer(f'{all_user_3}', parse_mode='HTML')
                await message.answer(f'{all_user_4}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
        else:
            await message.answer(f'На {event["name"]} пока никого не зарегестрировалось', reply_markup=create_backword_menu_kb())
            await state.clear()
    else:
        await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз', reply_markup=create_cancel_show_kb())


# Этот хэндлер будет срабатывать, если во время
# проверки анкеты будет введено что-то некорректное
@router.message(StateFilter(FSMShowRegistr))
async def warning_show_registr(message: Message):
    await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз', reply_markup=create_cancel_show_kb())






                                    # ФУНКЦИЯ БРОНИРОВАНИЯ СТОЛИКА







class FSMBooking(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    date_choosing = State() # Состояние выбора даты
    fill_guest = State()   # Cостояние ввода количества гостей
    fill_first_name = State()   # Cостояние ввода имени
    fill_last_name = State()       # Состояние ввода фамилии
    fill_bd = State()       # Состояние ввода даты рождения
    fill_phone = State()       # Состояние ввода номера телефона
    verification_form = State() # Состояние подтверждения заполненой формы
    section_choosing = State() # Состояние выбора раздела для внесения изменений


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить бронирование"
# и отменять процесс бронирования столика
@router.callback_query(Text(text='cancel_booking'), StateFilter(FSMBooking))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Бронирование отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
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
    await state.update_data(date=date, user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(f'На какое количетсво гостей хотите забронировать столик ?', reply_markup=create_cancel_booking_kb(), parse_mode='HTML')
    await state.set_state(FSMBooking.fill_guest)


# Этот хэндлер будет срабатывать, если во время
# проверки анкеты будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.date_choosing))
async def warning_date_choosing(message: Message):
    await message.answer(text=f'Выберите дату для продолжения бронирования столика или нажмите кнопку отменить', reply_markup=create_cancel_booking_kb())



# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMBooking.fill_guest), lambda x: x.text.isdigit())
async def process_fill_guest(message: Message, state: FSMContext, bot: Bot):
    guest = message.text
    users = select_users_id()
    db = await state.get_data()
    if str(message.from_user.id) in users:
        user = select_one_user(message.from_user.id)
        await message.answer(f'Заявка на бронирование столика отправлена администратору, после проверки наличия свободных мест мы свяжемся с вами🙂', parse_mode='HTML')
        for id in config.tg_bot.admin_ids:
            await bot.send_message(id, f'<b>{user["first_name"]} {user["last_name"]}</b> оставил(а) заявку на бронирование столика {db["date"]} на {guest} гостей\nНомер телефона: {user["phone"]}\nУникальный код пользователя: {user["id"]}', parse_mode='HTML')
        await state.clear()
    else:
        await message.answer(f'Вы выбрали дату - {db["date"]}\n\nВведите ваше имя', reply_markup=create_cancel_booking_kb())
        await state.update_data(guest=guest)
        await state.set_state(FSMBooking.fill_first_name)


# Этот хэндлер будет срабатывать, если во время
# ввода имени будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.fill_guest))
async def warning_fill_guest(message: Message):
    await message.answer(
        text=f'Количетсво гостей должно быть числом, введите количество гостей еще раз', reply_markup=create_cancel_booking_kb())




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
async def process_yes_button(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # добавляем нового пользователя в базу данных
    db = await state.get_data()
    insert_user(db['user_id'], db['first_name'], db['last_name'], db['birthday'], db['phone'])
    user = select_one_user(db['user_id'])
    await callback.message.delete()
    await callback.message.answer(f'Заявка на бронирование столика отправлена администратору, после проверки наличия свободных мест мы свяжемся с вами🙂', parse_mode='HTML')
    for id in config.tg_bot.admin_ids:
        await bot.send_message(id, f'<b>{user["first_name"]} {user["last_name"]}</b> оставил(а) заявку на бронирование столика {db["date"]} на {db["guest"]} гостей\nНомер телефона: {user["phone"]}\nУникальный код пользователя: {user["id"]}', parse_mode='HTML')
    await state.clear()



# этот хэндлер будет срабатывать на нажатие кнопки "нет" во время проверки заполнения анкеты
# при регистрации на мероприятие и отправлать список изменений
@router.callback_query(Text(text='no'), StateFilter(FSMBooking.verification_form))
async def process_yes_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f'Выберите раздел, в который хотите внести изменения:\n1 - изменить имя;\n2 - изменить фамилию;\n3 - изменить дату рождения;\n4 - изменить номер телефона;', reply_markup=create_cancel_booking_kb())
    await state.set_state(FSMBooking.section_choosing)



# Этот хэндлер будет срабатывать, если во время
# проверки анкеты будет введено что-то некорректное
@router.message(StateFilter(FSMBooking.verification_form))
async def warning_verification_form(message: Message):
    await message.answer(text=f'Для продолжения бронирования нажмите на кнопку да/нет', reply_markup=create_cancel_booking_kb())



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






                                    # ФУНКЦИЯ ДОБАВЛЕНИЯ БРОНИ СТОЛИКА






class FSMBookingTable(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    add_booking = State()       # Состояние добавления мероприятия



# Этот хэндлер будет срабатывать на отправку команды /addbooking
# и отправлять в чат правила добавления брони столика
@router.message(Command(commands='addbooking'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_addevent_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['addbooking'], reply_markup=create_cancel_addbooking_kb())
    await state.set_state(FSMBookingTable.add_booking)


# Этот хэндлер будет проверять правильность введенных данных
# и отправлять сообщение о добавлении фото
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMBookingTable.add_booking))
async def process_add_event(message: Message, state: FSMContext):
    add_list = [i.strip() for i in message.text.split(';')]
    if len(add_list) == 3:
        error = 0
        if not add_list[0].isdigit():
            await message.answer('Количество гостей должно быть числом', reply_markup=create_cancel_addbooking_kb())
            error += 1
        if not check_date(add_list[1]):
            await message.answer(f'Дата введена не в верном формате, введите дату в формате:\ndd.mm.yyyy', reply_markup=create_cancel_addbooking_kb())
            error += 1
        user_id = select_all_ids()
        if int(add_list[2]) not in user_id:
            await message.answer('Уникальный код пользователя указан не верно', reply_markup=create_cancel_addbooking_kb())
            error += 1
        if error == 0:
            user = select_user(add_list[2])
            insert_booking_table(user['first_name'], user['last_name'], add_list[0], add_list[1], user['phone'])
            await message.answer('Бронирование добавлено')
            # Завершаем машину состояний
            await state.clear()
    else:
        await message.answer(f'Введенные данные не корректны\n'
                             f'Скорее всего вы забыли поставить ; в конце одного из разделов или поставили лишний знак ;\n'
                             f'Сравните еще раз введенные данные с шаблоном и после исправления отправьте данные еще раз\n\n',
                             reply_markup=create_cancel_addbooking_kb())


# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMBookingTable.add_booking))
async def warning_addbooking(message: Message):
    await message.answer(text=f'Для добавления бронирования введите данные согласно шаблону', reply_markup=create_cancel_addbooking_kb())


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить добавление бронирования"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_addbooking'), StateFilter(FSMBookingTable))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Добавление бронирования отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
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
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Просмотр списка бронирований столиков отменен')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
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
    booking_table_list = []
    all_booking_table = select_booking_table(date)
    num = 1
    if len(all_booking_table) != 0:
        for book in all_booking_table:
            booking_table_list.append(f'{num}) Имя: {book["first_name"]}\nФамилия: {book["last_name"]}\nКоличество гостей: {book["guest"]}\nНомер телефона: {book["phone"]}')
            num += 1
        all_booking = f'\n\n'.join(booking_table_list)
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
    delete_card = State()    # Состояние удаления карты


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить добавление карты"
# и отменять процесс бронирования столика
@router.callback_query(Text(text='cancel_card'), StateFilter(FSMCard.add_card))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Добавление карты отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
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
    cards = sorted(cards, key=lambda x: x['card'])
    num = 1
    for card in cards:
        card_list.append(f'{num}) Номер клубной карты: {card["card"]}\nИмя: {card["first_name"]}\nФамилия: {card["last_name"]}\nДата рождения: {card["birthday"]}\nНомер телефона: {card["phone"]}')
        num += 1
    if len(card_list) <= 30:
        all_card = f'\n\n'.join(card_list)
        await message.answer(f'{all_card}', reply_markup=create_backword_menu_kb())
    elif len(card_list) >= 31 and len(card_list) <= 60:
        all_card_1 = f'\n\n'.join(card_list[0:30])
        all_card_2 = f'\n\n'.join(card_list[30:])
        await message.answer(f'{all_card_1}')
        await message.answer(f'{all_card_2}', reply_markup=create_backword_menu_kb())
    elif len(card_list) >= 61 and len(card_list) <= 90:
        all_card_1 = f'\n\n'.join(card_list[0:30])
        all_card_2 = f'\n\n'.join(card_list[30:60])
        all_card_3 = f'\n\n'.join(card_list[60:])
        await message.answer(f'{all_card_1}')
        await message.answer(f'{all_card_2}')
        await message.answer(f'{all_card_3}', reply_markup=create_backword_menu_kb())
    elif len(card_list) >= 91 and len(card_list) <= 120:
        all_card_1 = f'\n\n'.join(card_list[0:30])
        all_card_2 = f'\n\n'.join(card_list[30:60])
        all_card_3 = f'\n\n'.join(card_list[60:90])
        all_card_4 = f'\n\n'.join(card_list[90:])
        await message.answer(f'{all_card_1}')
        await message.answer(f'{all_card_2}')
        await message.answer(f'{all_card_3}')
        await message.answer(f'{all_card_4}', reply_markup=create_backword_menu_kb())
    elif len(card_list) >= 121 and len(card_list) <= 150:
        all_card_1 = f'\n\n'.join(card_list[0:30])
        all_card_2 = f'\n\n'.join(card_list[30:60])
        all_card_3 = f'\n\n'.join(card_list[60:90])
        all_card_4 = f'\n\n'.join(card_list[90:120])
        all_card_5 = f'\n\n'.join(card_list[120:])
        await message.answer(f'{all_card_1}')
        await message.answer(f'{all_card_2}')
        await message.answer(f'{all_card_3}')
        await message.answer(f'{all_card_4}')
        await message.answer(f'{all_card_5}', reply_markup=create_backword_menu_kb())
    elif len(card_list) >= 151 and len(card_list) <= 180:
        all_card_1 = f'\n\n'.join(card_list[0:30])
        all_card_2 = f'\n\n'.join(card_list[30:60])
        all_card_3 = f'\n\n'.join(card_list[60:90])
        all_card_4 = f'\n\n'.join(card_list[90:120])
        all_card_5 = f'\n\n'.join(card_list[120:150])
        all_card_6 = f'\n\n'.join(card_list[150:])
        await message.answer(f'{all_card_1}')
        await message.answer(f'{all_card_2}')
        await message.answer(f'{all_card_3}')
        await message.answer(f'{all_card_4}')
        await message.answer(f'{all_card_5}')
        await message.answer(f'{all_card_6}', reply_markup=create_backword_menu_kb())






                                 # Функция удаления владельцев клубных карт





# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить удаление карты"
# и отменять процесс бронирования столика
@router.callback_query(Text(text='cancel_card'), StateFilter(FSMCard.delete_card))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Удаление карты отменено')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать на отправку команды /deletecard
# и отправлять в чат правила удаления карты
@router.message(Command(commands='deletecard'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_deletecard_command(message: Message, state: FSMContext):
    text = 'Для удаления карты введите номер карты'
    await message.answer(text=text, reply_markup=create_cancel_delete_card_kb())
    await state.set_state(FSMCard.delete_card)



# Этот хэндлер будет проверять правильность введенных данных
# и отправлять сообщение об удалении владельца карты
@router.message(IsAdmin(config.tg_bot.admin_ids), StateFilter(FSMCard.delete_card),
lambda x: x.text.isdigit())
async def process_delete_card(message: Message, state: FSMContext):
    cards_num = []
    cards = select_all_cards()
    for card in cards:
        cards_num.append(card['card'])
    if int(message.text) in cards_num:
        try:
            delete_card(message.text)
            await message.answer('Владелец клубной карты удален', reply_markup=create_backword_menu_kb())
            # Завершаем машину состояний
            await state.clear()
        except:
            print('Произошла ошибка при удалении владельца клубной карты')
    else:
        await message.answer(f'Введенные данные не корректны, карты с таким номером нету\n', reply_markup=create_cancel_delete_card_kb())


# Этот хэндлер будет срабатывать, если во время
# ввода номера карты будет введено что-то некорректное
@router.message(StateFilter(FSMCard.delete_card))
async def warning_delete_card(message: Message):
    await message.answer(text=f'Для удаления карты введите номер карты', reply_markup=create_cancel_delete_card_kb())




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
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Рассылка отменена')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
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
        await message.answer('Добавьте фото или видео рассылки', reply_markup=create_cancel_newslatter_kb())
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
    elif message.video:
        db = await state.get_data()
        video = message.video.file_id
        await message.answer(f'Ниже представлена сформированная рассылка, введите:\n\n1 - чтобы отправить текущий вариант;\n2 - чтобы изменить текст;\n3 - чтобы изменить фото или видео', reply_markup=create_cancel_newslatter_kb())
        await message.answer_video(video=video, caption=db['text'])
        await state.update_data(video=video)
        # Устанавливаем состояние ожидания подтверждения сформированной рассылки
        await state.set_state(FSMNewsletter.verification_newslatter)
    else:
        await message.answer('Добавьте фото или видео рассылки', reply_markup=create_cancel_newslatter_kb())



# Этот хэндлер будет срабатывать на введенный номер раздела при подтверждении рассылки
@router.message(StateFilter(FSMNewsletter.verification_newslatter), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 3)
async def process_fill_phone(message: Message, state: FSMContext, bot: Bot):
    db = await state.get_data()
    if int(message.text) == 1:
        db = await state.get_data()
        users_id = select_users_id()
        for id in users_id:
            try:
                if 'photo' in db.keys():
                    await bot.send_photo(chat_id=id, photo=db['photo'], caption=db['text'])
                elif 'video' in db.keys():
                    await bot.send_video(chat_id=id, video=db['video'], caption=db['text'])
            except:
                print(f'Произошла ошибка при отправке рассылки на id - {id}')
        await message.answer('Рассылка отправлена', reply_markup=create_backword_menu_kb())
        await state.clear()
    elif int(message.text) == 2:
        await message.answer(f'Введите новый текст рассылки', reply_markup=create_cancel_newslatter_kb())
        # Устанавливаем состояние ввода текста рассылки
        await state.set_state(FSMNewsletter.create_text)
    elif int(message.text) == 3:
        await message.answer(f'Отправьте новое фото или видео рассылки', reply_markup=create_cancel_newslatter_kb())
        # Устанавливаем состояние добавления фото
        await state.set_state(FSMNewsletter.add_photo)


# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMNewsletter.verification_newslatter))
async def warning_fill_phone(message: Message):
    await message.answer(text=f'Для выбора раздела введите номер от 1 до 3', reply_markup=create_cancel_newslatter_kb())





                                 # Функция опроса пользователей после мероприятия





class FSMSurvey(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    question_1 = State()    # Состояние ожидания ответа на первый вопрос
    question_2 = State()    # Состояние ожидания ответа на второй вопрос
    question_3 = State()    # Состояние ожидания ответа на третий вопрос
    question_4 = State()    # Состояние ожидания ответа на четвертый вопрос
    question_5 = State()    # Состояние ожидания ответа на пятый вопрос


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить рассылку"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_survey'), StateFilter(FSMSurvey, default_state))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Опрос отмененен')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMSurvey))
async def warning_survey(message: Message):
    await message.answer(text=f'Вы находитесь в режиме опроса, чтобы использовать другие возможности бота пройдите опрос или отмените его', reply_markup=create_cancel_survey_kb())


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с оценкой
# во время ответа на первый вопрос
@router.callback_query(Text(text=['1', '2', '3', '4', '5']), StateFilter(default_state))
async def process_question_1_press(callback: CallbackQuery, state: FSMContext):
    question_1 = callback.data
    event_name = callback.message.text.split('"')
    await state.update_data(question_1=question_1, user_id=callback.from_user.id, event_name=event_name[1])
    await callback.message.delete()
    await callback.message.answer(f'Оцените качество алкоголя:', reply_markup=create_question_2_kb())
    await state.set_state(FSMSurvey.question_2)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с оценкой
# во время ответа на второй вопрос
@router.callback_query(Text(text=['1', '2', '3', '4', '5', '6']), StateFilter(FSMSurvey.question_2))
async def process_question_1_press(callback: CallbackQuery, state: FSMContext):
    if callback.data == '6':
        question_2 = callback.message.reply_markup.inline_keyboard[1][0].text
    else:
        question_2 = callback.message.reply_markup.inline_keyboard[0][int(callback.data) - 1].text
    await state.update_data(question_2=question_2)
    await callback.message.delete()
    await callback.message.answer(f'Оцените качество кальяна:', reply_markup=create_question_3_kb())
    await state.set_state(FSMSurvey.question_3)



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с оценкой
# во время ответа на третий вопрос
@router.callback_query(Text(text=['1', '2', '3', '4', '5', '6']), StateFilter(FSMSurvey.question_3))
async def process_question_1_press(callback: CallbackQuery, state: FSMContext):
    if callback.data == '6':
        question_3 = callback.message.reply_markup.inline_keyboard[1][0].text
    else:
        question_3 = callback.message.reply_markup.inline_keyboard[0][int(callback.data) - 1].text
    await state.update_data(question_3=question_3)
    await callback.message.delete()
    await callback.message.answer(f'Оцените качество обслуживания персонала:', reply_markup=create_question_kb())
    await state.set_state(FSMSurvey.question_4)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с оценкой
# во время ответа на четвертый вопрос
@router.callback_query(Text(text=['1', '2', '3', '4', '5']), StateFilter(FSMSurvey.question_4))
async def process_question_1_press(callback: CallbackQuery, state: FSMContext):
    question_4 = callback.data
    await state.update_data(question_4=question_4)
    await callback.message.delete()
    await callback.message.answer(f'Оцените качество работы охраны:', reply_markup=create_question_kb())
    await state.set_state(FSMSurvey.question_5)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки с оценкой
# во время ответа на пятый вопрос
@router.callback_query(Text(text=['1', '2', '3', '4', '5']), StateFilter(FSMSurvey.question_5))
async def process_question_1_press(callback: CallbackQuery, state: FSMContext):
    question_5 = callback.data
    db = await state.get_data()
    event_id = select_one_event_id(db['event_name'])
    user = select_one_user(db['user_id'])
    print(user)
    print(event_id)
    insert_survey(user['first_name'], user['last_name'], user['phone'], db['question_1'], db['question_2'], db['question_3'], db['question_4'], question_5, event_id)
    await callback.message.delete()
    await callback.message.answer(f'Спасибо за прохождение опроса, с помощью вас мы становимся лучше :)')
    await state.clear()






                                # ФУНКЦИЯ ПРОСМОТРА ОПРОСА









class FSMShowSurvey(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    event_choosing = State() # Состояние выбора мероприятия



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "Отменить просмотр"
# и отменять процесс регистрации на мероприятие
@router.callback_query(Text(text='cancel_show'), StateFilter(FSMShowSurvey))
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    photo = URLInputFile(url=LEXICON['menu_photo'])
    await callback.message.answer('Просмотр опроса отменен')
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        reply_markup=create_menu_kb(),
        parse_mode='HTML')
    # Завершаем машину состояний
    await state.clear()



# этот хэндлер будет срабатывать на команду /showsurvey
# и отправлять пользователю сообщение с выбором мероприятия
@router.message(Command(commands='showsurvey'), StateFilter(default_state), IsAdmin(config.tg_bot.admin_ids))
async def process_showsurvey_command(message: Message, state: FSMContext):
    events_list = []
    id_list = []
    num = 1
    events = select_all_events()
    if len(events) != 0:
        for event in events:
            try:
                if next_day_date_2() >= now_time(f'{event["date"]} 00:00'):
                    continue
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
            if len(events_list) <= 20:
                events = f'\n\n'.join(events_list)
                text = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                await message.answer(text=text, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
            elif len(events_list) >= 21 and len(events_list) <= 40:
                events_1 = f'\n\n'.join(events_list[0:20])
                events_2 = f'\n\n'.join(events_list[20:])
                text_1 = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events_1}"
                text_2 = f"{events_2}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                await message.answer(text=text_1,parse_mode='HTML')
                await message.answer(text=text_2, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
            elif len(events_list) >= 41 and len(events_list) <= 60:
                events_1 = f'\n\n'.join(events_list[0:20])
                events_2 = f'\n\n'.join(events_list[20:40])
                events_3 = f'\n\n'.join(events_list[40:])
                text_1 = f"<b>ВЫБЕРИТЕ МЕРОПРИЯТИЕ</b>\n\n{events_1}"
                text_2 = f"{events_2}"
                text_3 = f"{events_3}\n\n<i>ЧТОБЫ ВЫБРАТЬ МЕРОПРИЯТИЕ ВВЕДИТЕ КОД МЕРОПРИЯТИЯ</i>❗️"
                await message.answer(text=text_1, parse_mode='HTML')
                await message.answer(text=text_2, parse_mode='HTML')
                await message.answer(text=text_3, reply_markup=create_cancel_show_kb(),parse_mode='HTML')
            # Устанавливаем состояние ожидания выбора мероприятия
            await state.set_state(FSMShowSurvey.event_choosing)
            await state.update_data(id_list=id_list)
    else:
        await message.answer("К сожалению на данный момент запланированных мероприятий нет, попробуйте проверить позже.")




# Этот хэндлер будет срабатывать, если введен корректный номер мероприятия
@router.message(StateFilter(FSMShowSurvey.event_choosing), lambda x: x.text.isdigit())
async def process_event_choosing(message: Message, state: FSMContext):
    db = await state.get_data()
    id_list = db['id_list']
    survey_list = []
    if int(message.text) in id_list:
        event = select_one_event(message.text)
        survey_all = select_survey(message.text)
        print(survey_all)
        num = 1
        for survey in survey_all:
            survey_list.append(f'{num}) <b>Имя</b>: {survey["first_name"]}\n<b>Фамилия</b>: {survey["last_name"]}\n<b>Номер телефона</b>: {survey["phone"]}\n<b>Качество музыки</b>: {survey["question_1"]}\n<b>Качество алкоголя</b>: {survey["question_2"]}\n<b>Качество кальяна</b>: {survey["question_3"]}\n<b>Качество обслуживание персонала</b>: {survey["question_4"]}\n<b>Качество работы охраны</b>: {survey["question_5"]}\n')
            num += 1
        if len(survey_list) != 0:
            if len(survey_list) <= 15:
                final_list = f'\n\n'.join(survey_list)
                await message.answer(f'На {event["name"]} прошли опрос:\n\n{final_list}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
            elif len(survey_list) >= 15 and len(survey_list) <= 30:
                final_list_1 = f'\n\n'.join(survey_list[0:15])
                final_list_2 = f'\n\n'.join(survey_list[15:])
                await message.answer(f'На {event["name"]} прошли опрос:\n\n{final_list_1}', parse_mode='HTML')
                await message.answer(f'{final_list_2}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
            elif len(survey_list) >= 30 and len(survey_list) <= 45:
                final_list_1 = f'\n\n'.join(survey_list[0:15])
                final_list_2 = f'\n\n'.join(survey_list[15:30])
                final_list_3 = f'\n\n'.join(survey_list[30:])
                await message.answer(f'На {event["name"]} прошли опрос:\n\n{final_list_1}', parse_mode='HTML')
                await message.answer(f'{final_list_2}', parse_mode='HTML')
                await message.answer(f'{final_list_3}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
            elif len(survey_list) >= 45 and len(survey_list) <= 60:
                final_list_1 = f'\n\n'.join(survey_list[0:15])
                final_list_2 = f'\n\n'.join(survey_list[15:30])
                final_list_3 = f'\n\n'.join(survey_list[30:45])
                final_list_4 = f'\n\n'.join(survey_list[45:])
                await message.answer(f'На {event["name"]} прошли опрос:\n\n{final_list_1}', parse_mode='HTML')
                await message.answer(f'{final_list_2}', parse_mode='HTML')
                await message.answer(f'{final_list_3}', parse_mode='HTML')
                await message.answer(f'{final_list_4}', reply_markup=create_backword_menu_kb(), parse_mode='HTML')
                await state.clear()
        else:
            await message.answer(f'На "{event["name"]}" пока не проходили опрос', reply_markup=create_backword_menu_kb())
            await state.clear()
    else:
        await message.answer(text=f'Введен не верный код мероприятия, попробуйте еще раз', reply_markup=create_cancel_show_kb())



# Этот хэндлер будет срабатывать, если во время
# ввода номера раздела внесения изменений будет введено что-то некорректное
@router.message(StateFilter(FSMShowSurvey.event_choosing))
async def warning_show_survey(message: Message):
    await message.answer(text=f'Для выбора мероприятия, введите код мероприятия', reply_markup=create_cancel_show_kb())

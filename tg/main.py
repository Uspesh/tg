import logging
from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown, executor
from cart import Cart
from content.text import *
from keybords import *
from tg.calendar.google_api import calendar, calendar_id
import datetime
from tg.calendar.datatime_work import get_calendar
from config import API_TOKEN
from states import BookingTime
from aiogram.dispatcher.filters import state


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(text='Назад')
@dp.message_handler(commands=['start', 'help'])
async def return_start_info(message: types.Message):
    '''
    Начало работы с клиентом, возвращает кнопки, фотки студии и описание студии
    '''

    await types.ChatActions.upload_photo()

    media_group = types.MediaGroup()

    global cart
    global list_buttons  # выбранные доп. услуги
    global user_data
    cart = Cart(chat_id=message.chat.id)
    list_buttons = []
    user_data = dict()

    for path in photos_path:
        media_group.attach_photo(types.InputFile(path))
    if message.text in ('/start', 'Назад'):
        await message.answer_media_group(media=media_group)
        await message.answer(markdown.text(about_st), reply_markup=choose_service_buttons)
    if message.text == '/help':
        await message.answer(markdown.text(contacts))


@dp.message_handler(text=['Студия', 'Только циклорама', 'Студия и гримерка'])
async def choose_service(message: types.Message):
    '''При выборе того, что в text, возвращает кнопки с доп.услугами. При нажатии на кнопку без доп. услуг переходим к расписанию'''
    list_buttons.append(message.text)
    await message.answer(markdown.text(optional_services), reply_markup=optional_service_buttons)


@dp.message_handler(text=['Дым', 'Проектор', 'Диско-шар', 'Латексный фон', 'Гардероб'])
async def list_of_chosen_services(message: types.Message):
    '''Добавляем товар в корзину, повторно возвращаем кнопки с доп товарами, если нажимается кнопка - этого достаточно, переходим к броне'''
    text = 'Еще что-то?'
    if message.text in list_buttons:
        chosen_items = ', '.join(str(elem) for elem in list_buttons)
        warning = f'Вы не можете выбрать 2 одинаковых услуги.\nВыберите другую услугу или нажмите на кнопку - этого достаточно.\nВыбранные услуги - {chosen_items}'
        await message.answer(markdown.text(warning), reply_markup=choose_optional_service_buttons)
    else:
        list_buttons.append(message.text)
        await message.answer(markdown.text(text), reply_markup=choose_optional_service_buttons)


@dp.message_handler(text=['Без доп. услуг', 'Этого достаточно', 'Гримерка'])
async def choose_booking_time(message: types.Message):
    if message.text == 'Этого достаточно':
        for service in list_buttons[1:]:
            cart.add_to_cart(chat_id=message.chat.id, service_name=service, service_price=price_dict[service])
    if message.text == 'Гримерка':
        list_buttons.append(message.text)
        cart.add_to_cart(chat_id=message.chat.id, service_name=list_buttons[0], service_price=price_dict[list_buttons[0]])

    await message.answer(markdown.text(calendar_text), reply_markup=await get_time_buttons())


@dp.callback_query_handler(text_startswith=["time_current_", 'time_next_'])
async def calendar_tap(call: types.CallbackQuery):
    '''
    Метод показывает юзеру занятое время на выбранный день
    '''

    query_current_date = call.data.split("_")[2]
    month = datetime.date.today().month
    month_for_calendar = str(month).zfill(2)
    month_for_client = month
    day = None

    if call.data.startswith('time_next_'):
        month_for_calendar = str(int(str(datetime.date.today().month)) + 1).zfill(2)
        month_for_client = int(str(datetime.date.today().month)) + 1

    if len(query_current_date) == 1:
        day = f'{str(query_current_date).zfill(2)}'
    else:
        day = query_current_date

    if month:
        current_date = f'{str(datetime.date.today())[:-5]}{month_for_calendar}-{day}'
    else:
        current_date = f'{str(datetime.date.today())[:-2]}{day}'

    timeMin = f'{current_date}T09:00:00+03:00'
    timeMax = f'{current_date}T22:00:00+03:00'
    user_data['booking_date'] = f'{str(datetime.date.today())[:-5]}{month_for_calendar}-{day}'

    events = get_calendar(timeMin=timeMin, timeMax=timeMax)
    free_time = ''
    time_slots = ''
    for event in events:
        start_event = event['start'][-14:-9]
        end_event = event['end'][-14:-9]
        time_slots += f'{start_event} - {end_event}\n'

    min_time = min_studio_booking_time if list_buttons[0] in ('Студия', 'Только циклорама') else min_booking_time

    if len(time_slots) < 1:
        time_slots = f'Весь {int(day)} день {month_for_client}-го месяца свободен'
        free_time = f'\n\n{time_slots}\nВремя работы студии с {timeMin[-14:-9]} до {timeMax[-14:-9]}\n\nВсе время работы доступно для записи. {min_time}'

    else:
        free_time = f'''
            Выберите время съемки.\n\nНа {int(day)} число {month_for_client}-го месяца, забронированное время с:\n{time_slots}\nВремя работы студии с {timeMin[-14:-9]} до {timeMax[-14:-9]}\n\nВсе не занятое время работы доступно для записи.{min_time}
        '''

    await bot.edit_message_text(chat_id=call.from_user.id,
                                text=markdown.text(free_time),
                                message_id=call.message.message_id,
                                reply_markup=await back_button())


@dp.callback_query_handler(text="back")
async def back(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.from_user.id,
                                text=markdown.text(calendar_text),
                                reply_markup=await get_time_buttons(),
                                message_id=call.message.message_id)


@dp.callback_query_handler(text='booking_time')
async def booking_time(call: types.CallbackQuery):
    short_text = min_booking_time if list_buttons[0] not in ('Студия', 'Только циклорама') else min_studio_booking_time
    await bot.edit_message_text(
        chat_id=call.from_user.id,
        text=f"{booking_time_text}{short_text}",
        message_id=call.message.message_id
    )

    await BookingTime.booking_time.set()


@dp.message_handler(state=BookingTime.booking_time)
async def get_booking_time(message: types.Message, state: FSMContext):
    timeMin = str(message.text.split('-')[0].strip()) #[:5]
    timeMax = str(message.text.split('-')[1].strip()) #[8:]
    booking_hours = None

    try:
        if datetime.datetime.strptime(timeMin, '%H:%M') and datetime.datetime.strptime(timeMax, '%H:%M'):
            booking_hours = datetime.datetime.strptime(timeMax, '%H:%M') - datetime.datetime.strptime(timeMin, '%H:%M')

            if list_buttons[0] not in ('Студия', 'Только циклорама') and '0:30:00' <= str(booking_hours) < '1:00:00':
                await message.answer(markdown.text(f'Вы выбрали {list_buttons[0]}, на 30 минут можно забронировать только Студию или циклораму.'))

            elif list_buttons[0] not in ('Студия', 'Только циклорама') and str(booking_hours) >= '1:00:00':
                await state.finish()
                user_data['timeMin'] = timeMin
                user_data['timeMax'] = timeMax
                time_int = int(str(booking_hours)[0])
                cart.add_to_cart(chat_id=message.chat.id, service_name=list_buttons[0],
                                 service_price=price_dict[list_buttons[0]] * time_int)

                await message.answer(markdown.text('Вы все ввели правильно, нажмите продолжить для оформления брони.'),
                                     reply_markup=continue_button)


            elif list_buttons[0] in ('Студия', 'Только циклорама') and str(booking_hours) >= '0:30:00': #1:00:00 0:30:00
                user_data['timeMin'] = timeMin
                user_data['timeMax'] = timeMax
                await state.finish()
                if str(booking_hours) == '0:30:00':
                    cart.add_to_cart(chat_id=message.chat.id, service_name=list_buttons[0], service_price=700)
                elif str(booking_hours) >= '1:00:00':
                    time_int = int(str(booking_hours)[0])
                    cart.add_to_cart(chat_id=message.chat.id, service_name=list_buttons[0], service_price=price_dict[list_buttons[0]] * time_int)

                await message.answer(markdown.text('Вы все ввели правильно, нажмите продолжить для оформления брони.'), reply_markup=continue_button)

    except Exception as ex:
        await message.answer(markdown.text(f'Вы ввели не правильноe время для записи.\n\n{booking_time_text}'))


@dp.message_handler(text='Продолжить')
async def get_user_name(message: types.Message):
    await message.answer(text=get_user_full_name, reply_markup=types.ReplyKeyboardRemove())
    await BookingTime.name.set()


@dp.message_handler(state=BookingTime.name)
async def set_user_name(message: types.Message, state: FSMContext):
    name = message.text
    user_data['name'] = name

    await state.finish()
    await message.answer(text=get_user_phone_number)
    await BookingTime.phone_number.set()


@dp.message_handler(state=BookingTime.phone_number)
async def set_user_phone_number(message: types.Message, state: FSMContext):
    number = message.text

    if (len(number) == 11 and number[0] == '8') or (len(number) == 12 and number[0] == '+'):
        user_data['phone_number'] = number
        await state.finish()
        await message.answer(markdown.text("Нажмите оплата, если готовы перейти к оплате или назад, если ввели что то неправильно и хотите вернуться в самое начало."), reply_markup=go_to_payment)
    else:
        await message.answer(markdown.text('Вы ввели номер телефона не правильно. Пожалуйста начните ввод номера телефона с 8 или +7'))


@dp.message_handler(text=['Абонемент'])
async def reply_about_season(message: types.Message):
    list_buttons.append(message.text)
    await message.answer(markdown.text(text_season), reply_markup=seasons)


@dp.message_handler(text=['Фотограф'])
async def book_photograph(message: types.Message):
    photo = types.InputFile('./content/about_st_photo/photograph.jpg')
    await message.answer_photo(photo = photo)
    await message.answer(text=photograph_info)
    await message.answer(text=photograph_booking, reply_markup=back_to_begin_button)


@dp.message_handler(text=['5 часов', '10 часов', '15 часов', 'Оплата'])
async def payment_requirements(message: types.Message):
    chosen_season_time = None
    if message.text != 'Оплата':
        cart.add_to_cart(chat_id=message.chat.id, service_price=price_dict[message.text], service_name=f'Абонемент на {message.text}')
    chosen_items = ', '.join(str(elem) for elem in list_buttons)

    for i in cart.total_services(chat_id=message.chat.id):
        chosen_season_time = i

    price_check = cart.total_price(chat_id=message.chat.id)
    if list_buttons[0] != 'Абонемент':
        await message.answer(f'Ваша корзина - {chosen_items}, стоимость которой составляет - {price_check}\n\n{payment_text}', reply_markup=apply_button)
    else:
        await message.answer(markdown.text(f'Ваша корзина - {chosen_season_time}, стоимость которой составляет - {price_check}\n\n{payment_text}.\n\nДля оформления новой брони нажмите кнопку /start в Меню.'), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text='Подтвердить')
async def create_event_after_all(message: types.Message):
    timeMin = f"{user_data['booking_date']}T{user_data['timeMin']}:00+03:00"
    timeMax = f"{user_data['booking_date']}T{user_data['timeMax']}:00+03:00"
    summary = f'Бронь с {user_data["timeMin"]} по {user_data["timeMax"]}'
    description = f'{user_data["name"]} - {user_data["phone_number"]}'
    calendar.add_event(calendar_id=calendar_id, time_start=timeMin, time_end=timeMax, summary=summary, description=description)
    chosen_items = ', '.join(str(elem) for elem in list_buttons[1:])
    if len(chosen_items) > 1:
        await message.answer(markdown.text(f'Вы успешно забронировали {list_buttons[0]} на время {user_data["timeMin"]} - {user_data["timeMax"]}, с услугами - {chosen_items}.\n\nДля оформления новой брони нажмите кнопку /start в Меню.'), reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(markdown.text(
            f'Вы успешно забронировали {list_buttons[0]} на время {user_data["timeMin"]} - {user_data["timeMax"]}.\n\nДля оформления новой брони нажмите кнопку /start в Меню.'),
                             reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import calendar
from dateutil.relativedelta import relativedelta

choose_service_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Студия'),
    types.KeyboardButton('Только циклорама'),
    types.KeyboardButton('Гримерка'),
    types.KeyboardButton('Студия и гримерка'),
    types.KeyboardButton('Фотограф'),
    types.KeyboardButton('Абонемент'),
)

optional_service_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Дым'),
    types.KeyboardButton('Проектор'),
    types.KeyboardButton('Диско-шар'),
    types.KeyboardButton('Латексный фон'),
    types.KeyboardButton('Гардероб'),
    types.KeyboardButton('Без доп. услуг')
)

choose_optional_service_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Дым'),
    types.KeyboardButton('Проектор'),
    types.KeyboardButton('Диско-шар'),
    types.KeyboardButton('Латексный фон'),
    types.KeyboardButton('Гардероб'),
    types.KeyboardButton('Этого достаточно')
)

seasons = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('5 часов'),
    types.KeyboardButton('10 часов'),
    types.KeyboardButton('15 часов'),
    types.KeyboardButton('Назад')
)

continue_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Продолжить')
)

go_to_payment = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Оплата'),
    types.KeyboardButton('Назад')
)

apply_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Подтвердить')
)

back_to_begin_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Назад')
)

def create_keyboard(button1='', button2='', button3='', button4='', button5='', button6='', button7='', button8=''):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [button1, button2, button3, button4, button5, button6, button7, button8]
    for button in buttons:
        if len(button) > 1:
            keyboard.add(types.KeyboardButton(button))
    return keyboard


async def get_time_buttons():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=5)
    month_day = 1
    if str(datetime.date.today())[5:7] in ('01', '03', '05', '07', '08', '10', '12'):
        month_day = 31
    elif str(datetime.date.today())[5:7] in ('04', '06', '09', '11'):
        month_day = 30
    elif str(datetime.date.today())[5:7] == '02':
        month_day = 29 if calendar.isleap(int(str(datetime.date.today())[:4])) else 28

    # today = datetime.date.today()
    # last_day = today + datetime.timedelta(days=month_day)
    #
    # first_day = int(str(today)[8:])
    # end_day = int(str(last_day)[8:])
    today = datetime.date.today()
    end_second_month = today.day + 7 #(month_day - today.day)
    end_day = today.replace(day=month_day).replace(day=1) + relativedelta(months=1) + datetime.timedelta(days=end_second_month)
    end_day = end_day - datetime.timedelta(days=end_day.day)

    first_day = today.day
    # end_day = months_day.day + 1

    for date in range(first_day, end_day.day + 1):
        keyboard.insert(InlineKeyboardButton(text=str(date), callback_data=f"time_current_{date}"))

    for dates in range(1, end_second_month + 1):
        keyboard.insert(InlineKeyboardButton(text=str(dates), callback_data=f'time_next_{dates}'))
    return keyboard


async def back_button():
    return InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton(text="Назад", callback_data=f"back"),
        InlineKeyboardButton(text='Забронировать время', callback_data=f'booking_time')
    )


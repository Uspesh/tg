from pprint import pprint

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


def check_month_days(month: int):
    month_day = 1
    if month in (1, 3, 5, 7, 8, 10, 12):
        month_day = 31
    elif month in (4, 6, 9, 11): #[5:7]
        month_day = 30
    elif month == 2:
        month_day = 29 if calendar.isleap(int(str(datetime.date.today().year))) else 28

    return month_day

def get_time_buttons():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=5)
    current_month_day = check_month_days(datetime.date.today().month)

    today = datetime.date.today()

    second_month = today.month + 1
    second_month_days = check_month_days(second_month)

    end_second_month = today.day + 7 #(month_day - today.day)
    #end_day = today.replace(day=1) + relativedelta(months=1) + datetime.timedelta(days=end_second_month)
    end_day = today.replace(day=1, month=second_month) + datetime.timedelta(days=end_second_month)
    #print(end_day)
    end_day = end_day - datetime.timedelta(days=end_day.day)

    first_day = today.day
    # end_day = months_day.day + 1

    for date in range(first_day, current_month_day + 1):
        keyboard.insert(InlineKeyboardButton(text=str(date), callback_data=f"time_current_{date}"))

    for dates in range(1, end_second_month + 1):
        if dates > second_month_days:
            break
        keyboard.insert(InlineKeyboardButton(text=str(dates), callback_data=f'time_next_{dates}'))

    #print(current_month_day, second_month_days)
    #print(end_day)
    return keyboard

pprint(get_time_buttons())

async def back_button():
    return InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton(text="Назад", callback_data=f"back"),
        InlineKeyboardButton(text='Забронировать время', callback_data=f'booking_time')
    )


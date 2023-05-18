from aiogram.dispatcher.filters.state import State, StatesGroup

class BookingTime(StatesGroup):
    booking_time = State()
    name = State()
    phone_number = State()
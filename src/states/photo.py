from telebot.states import State, StatesGroup


class PhotoStates(StatesGroup):
    waiting_for_photo = State()
    resizing_photo = State()

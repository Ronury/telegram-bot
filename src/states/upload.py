from telebot.states import State, StatesGroup


class UploadStates(StatesGroup):
    waiting_for_file = State()
    processing_file = State()

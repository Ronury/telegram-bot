from telebot import TeleBot
from telebot.types import Message
from telebot.states.sync.context import StateContext

from src.states import UploadStates
from src.utils.logger import logger


def upload_handler(msg: Message, state: StateContext, bot: TeleBot):
    logger.info(f"User {msg.chat.id} pressed upload button")
    state.set(UploadStates.waiting_for_file)
    bot.send_message(msg.chat.id, 'Пожалуйста, загрузите рентгеновский снимок в формате JPG или PNG.')


def check_status(msg: Message, state: StateContext, bot: TeleBot):
    logger.info(f"User {msg.chat.id} pressed check button")
    current_state = state.get()
    if current_state == 'UploadStates:processing_file':
        bot.send_message(msg.chat.id, 'Анализ вашего снимка еще не завершен. '
                                      'Ожидайте, пожалуйста.' 
                                      'Обычно это занимает от 1 до 5 минут.')
    else:
        bot.send_message(msg.chat.id, 'Вы не вызвали /upload.')
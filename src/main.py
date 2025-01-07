import os

from dotenv import load_dotenv
import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from telebot.states.sync.middleware import StateMiddleware

from src.core import config
from src.states import UploadStates
from src.utils.logger import logger
from src.handlers import (
    start_handler, 
    show_help,
    upload_handler,
    check_status,
    send_feedback_form,
    process_rating,
    photo_handler
)


load_dotenv()


# Bot creation
STATE_STORAGE = StateMemoryStorage()
BOT = telebot.TeleBot(token=os.environ["TOKEN"], state_storage=STATE_STORAGE, use_class_middlewares=True)

# System handlers
BOT.register_message_handler(start_handler, commands=['start'], pass_bot=True)
BOT.register_message_handler(show_help, commands=['help'], pass_bot=True)

# Upload handlers
BOT.register_message_handler(upload_handler, commands=['upload'], pass_bot=True)
BOT.register_message_handler(check_status, commands=['status'], pass_bot=True)

# Feedback handlers
BOT.register_message_handler(send_feedback_form, commands=['feedback'], pass_bot=True)
BOT.register_callback_query_handler(callback=process_rating, func=lambda call: call.data.startswith("rating_"), pass_bot=True)

# Photo handlers
BOT.register_message_handler(photo_handler, content_types=['photo', 'text', 'document'], state=UploadStates.waiting_for_file, pass_bot=True)


BOT.add_custom_filter(custom_filters.StateFilter(BOT))
BOT.setup_middleware(StateMiddleware(BOT))

logger.info("Bot started")

BOT.polling(
    none_stop=config.NON_STOP, 
    long_polling_timeout=config.LONG_POLLING_TIMEOUT, 
    timeout=config.TIMEOUT, 
    interval=config.INTERVAL
)

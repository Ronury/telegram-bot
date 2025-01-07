from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.core import config
from src.utils.logger import logger


def send_feedback_form(msg: Message, bot: TeleBot):
    logger.info(f"User {msg.chat.id} pressed feedback button")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⭐️", callback_data="rating_1"),
               InlineKeyboardButton("⭐️⭐️", callback_data="rating_2"),
               InlineKeyboardButton("⭐️⭐️⭐️", callback_data="rating_3"),
               InlineKeyboardButton("⭐️⭐️⭐️⭐️", callback_data="rating_4"),
               InlineKeyboardButton("⭐️⭐️⭐️⭐️⭐️", callback_data="rating_5"))
    bot.reply_to(msg, "Оцените наше приложение:", reply_markup=markup)

def process_rating(call: Message, bot: TeleBot):
    rating = call.data.split("_")[1]

    logger.info(f"User {call.message.chat.id} gave us {rating} stars")

    bot.edit_message_text(
        chat_id=call.message.chat.id, 
        message_id=call.message.id,
        text=f"Спасибо за вашу оценку! Вы поставили {rating} звезд."
    )

from telebot import TeleBot
from telebot.types import Message

from src.utils.logger import logger


def start_handler(msg: Message, bot: TeleBot):
    logger.info(f"User {msg.chat.id} pressed start button")
    bot.send_message(msg.chat.id, 'Привет! Я бот для анализа рентгеновских снимков.'
                                  'Вы можете загрузить свое изображение, и я помогу вам с его анализом.'
                                  ' Напишите /help, чтобы узнать больше о командах.')

def show_help(msg: Message, bot: TeleBot):
    logger.info(f"User {msg.chat.id} pressed help button")
    help_text = (
        "*Доступные команды:*\n"
        "🔹 /upload - загрузить рентгеновский снимок для анализа\n"
        "🔹 /status - проверить статус анализа\n"
        "🔹 /help - получить помощь по использованию бота"
    )
    bot.send_message(msg.chat.id, help_text, parse_mode='Markdown')

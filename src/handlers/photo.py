from io import BytesIO

import numpy as np
from PIL import Image
from telebot import TeleBot
from telebot.types import Message
from telebot.states.sync.context import StateContext

from src.core import config
from src.states import UploadStates
from src.utils.logger import logger


def photo_handler(msg: Message, state: StateContext, bot: TeleBot):
    if msg.text:
        bot.send_message(msg.chat.id, "Пожалуйста, отправьте изображение, а не текст.")
        return

    elif msg.document:
        file_extension = msg.document.file_name.split(".")[-1].lower()
        if file_extension not in ['jpg', 'jpeg', 'png']:
            bot.send_message(msg.chat.id, "Пожалуйста, отправьте изображение в формате JPG или PNG.")
            return
        file_id = msg.document.file_id

    elif msg.photo:
        file_id = msg.photo[-1].file_id
    
    logger.info(f"User {msg.chat.id} sent photo")
    bot.send_message(msg.chat.id, "Спасибо! Я получил ваш рентгеновский снимок."
                                    "Начинаю анализ... Пожалуйста, подождите.")
    bot.send_chat_action(msg.chat.id, 'typing')
    state.set(UploadStates.processing_file)
    
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image = Image.open(BytesIO(downloaded_file))
    try:
        image = Image.open(BytesIO(downloaded_file))
        modified_image = image.convert('L').resize((512, 512), resample=Image.Resampling.LANCZOS)
    except Exception as e:
        logger.info(f"Got an error {e} with request done by {msg.chat.id}")
        bot.send_message(msg.chat.id, "Произошла ошибка при обработке изображения. Попробуйте загрузить его снова.")
        state.delete()
        return

    modified_image = image.convert('L').resize((512, 512), resample=Image.Resampling.LANCZOS)

    image_array = np.array(modified_image)
    image_array1 = np.expand_dims(image_array, axis=-1)
    image_array2 = np.expand_dims(image_array1, axis=0)

    try:
        prediction = config.MODEL.predict(image_array2)
    except Exception as e:
        logger.info(f"Got an error {e} with request done by {msg.chat.id}")
        bot.send_message(msg.chat.id, "Произошла ошибка при анализе изображения. Попробуйте снова.")
        return
    finally:
        state.delete()
        
    logger.info(f"The model gave a probability of {round(prediction[0][0], 4)}")

    if prediction[0][0] >= 0.7:
        bot.send_message(msg.chat.id,
                            'Анализ завершен!'
                            'На представленном рентгеновском снимке присутствует перелом.')
    else:
        bot.send_message(msg.chat.id,
                            'Анализ завершен! На представленном рентгеновском снимке отсутствует перелом.')

    state.delete()
    return

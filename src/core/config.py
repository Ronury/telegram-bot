from pathlib import Path

import tensorflow as tf


class Config:
    # Model settings
    MODEL_PATH = Path("./data/models/beta_binary_classifier.h5")

    # Logging
    LOGS_PATH = Path("./data/logs")

    # Bot settings
    LONG_POLLING_TIMEOUT = 60
    TIMEOUT = 20
    INTERVAL = 1
    NON_STOP = True

    # Model
    MODEL = tf.keras.models.load_model(MODEL_PATH)

config = Config()

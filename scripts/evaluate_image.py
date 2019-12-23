from __future__ import absolute_import, division, print_function, unicode_literals
from PIL import Image
from skimage import transform
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

labels = [
    "Angry",
    "Bank",
    "Fitness",
    "Book",
    "Car",
    "Electronics",
    "Happy",
    "Hotel",
    "Money",
    "Nature",
    "Relieved",
    "Sad",
    "Sick",
    "Singing",
    "Swimming",
    "Theatre",
]
emoji_model = tf.keras.experimental.load_from_saved_model(
    "./model", custom_objects={"KerasLayer": hub.KerasLayer}
)


def load_img(file_storage_object):
    np_img = Image.open(file_storage_object)
    np_img = np.array(np_img).astype("float32") / 255
    np_img = transform.resize(np_img, (224, 224, 3))
    np_img = np.expand_dims(np_img, axis=0)
    statistics = emoji_model.predict(np_img)[0]
    result_as_dict = dict(zip(labels, statistics.tolist()))

    return result_as_dict

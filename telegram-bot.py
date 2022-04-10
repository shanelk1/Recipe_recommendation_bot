# importing the required libraries for telegram

from telegram.ext import Updater, Filters, CommandHandler, MessageHandler

from tensorflow.keras.preprocessing import image_dataset_from_directory
import pickle
import pandas as pd
from tensorflow import keras
model = keras.models.load_model(
    '../Jay-branch/model_veg_fruits')
# creating the updater instance to use our bot api key

updater = Updater('5216349249:AAFjRqBdu3VkZJbHRr2Xa-WdH99iXhbvLbk')
dispatcher = updater.dispatcher

# Define all the different commands to be used by the bot


def start(updater, context):
    updater.message.reply_text(
        'Welcome to our Beta Chef bot! We are still in Beta so please bare with us')


def helper(updater, context):
    updater.message.reply_text(
        'Send me an image of an ingredient and I will try to tell you what it is')


def process_photo(updater, context):
    photo = updater.message.photo[-1].get_file()
    photo.download(
        'test_image/jalepeno/img.jpg')

    test_image_df = image_dataset_from_directory(
        directory='test_image',
        labels='inferred',
        label_mode='categorical',
        seed=5,
        color_mode="rgb",
        shuffle=True,
        batch_size=32,
        image_size=(100, 100)
    )

    labels_df = pd.read_csv('labels.csv')

    label = labels_df.iloc[model.predict(test_image_df).argmax()]
    label = label.ingredient

    updater.message.reply_text(f'Your ingredient is a {label}')


dispatcher.add_handler(CommandHandler('Start', start))
dispatcher.add_handler(CommandHandler('Help', helper))


dispatcher.add_handler(MessageHandler(Filters.photo, process_photo))


# start the telegram bot

updater.start_polling()
updater.idle()

# importing the required libraries for telegram

from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import tensorflow as tf
from tensorflow.keras.preprocessing import *
import pickle
import pandas as pd
import numpy as np
import requests as rq
from tensorflow import keras
from tensorflow.keras.applications.xception import decode_predictions
import os
from dotenv import load_dotenv

# importing Xception model
model = tf.keras.applications.Xception(
    include_top=True,
    weights="imagenet",
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",
)

# creating the updater instance to use our bot api key
load_dotenv()
telegram_api = os.getenv("telegram-api")
updater = Updater(telegram_api)
dispatcher = updater.dispatcher

# Define all the different commands to be used by the bot

# welcome messege /start


def start(updater, context):
    updater.message.reply_text(
        'Welcome to our Beta Chef bot! We are still in Beta so please bare with us')

# help command with insutrcions on how the bot works /help


def helper(updater, context):
    updater.message.reply_text(
        'This works in two ways \n 1. Send it an image of some ingredients and it will attempt to recognize whats in the image \n 2.Send a list of 2 or more ingredients separated by a comma (,) and it will look up a random recipe from Allrecipes.com')

# instance to wait for any image sent to attempt and classify it using the model loaded above


def process_photo(updater, context):
    photo = updater.message.photo[-1].get_file()
    photo_loc = photo.download('test_image/class1/img.jpg')


# preprocess the image for Xception model
    image = tf.keras.preprocessing.image.load_img(
        photo_loc, target_size=(299, 299))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.xception.preprocess_input(image)
# get the model labels
    response = rq.get(
        'https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json')
    imgnet_map = response.json()
    imgnet_map = {v[1]: k for k, v in imgnet_map.items()}

    prediction = model.predict(np.array([image]))
    label = decode_predictions(prediction, top=5)

    updater.message.reply_text(
        f'Your sent an image of what seems to have a {label[0][0][1]} .  Since we are in beta please go ahead and write a list of ingredients for me')

# instance that takes the user text input and then scrapes the all recipes website to return a randoom recipe
# this is utilizes a python module developed by @hhursev  from https://github.com/hhursev/recipe-scrapers


def get_responce(updater, context):
    updater.message.reply_text(
        'let me suggest some foods for you based on what you sent')
    text = updater.message.text
    ingredients = text.split(',')

    from bs4 import BeautifulSoup
    import random
    import requests as rq
    import json
    from recipe_scrapers import scrape_me

    sentence = "&IngIncl="
    http_start = 'https://www.allrecipes.com/search/results/?search='

    ingredients = [sentence + i for i in ingredients]
    ingredients = "".join(ingredients)
    ingredients
    url = http_start + ingredients

    request = rq.get(url)

    soup = BeautifulSoup(request.text, 'html.parser')

    recipes = []

    for a in soup.find_all('a', href=True):
        recipes.append(a['href'])

    recipes_df = pd.DataFrame(recipes)
    recipes_df.columns = ['url']
    recipes_df = recipes_df.loc[recipes_df['url'].str.contains('/recipe/')]
    recipes_df.reset_index(inplace=True)

    random = random.randint(0, len(recipes_df))
    scrape = scrape_me(recipes_df['url'][random])
    title = scrape.title()

    instructions = scrape.instructions()
    
    import spoonacular as sp
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api = sp.API(os.getenv(spoonacular-key))
    
    api.

    updater.message.reply_text(
        f'You can make ** {title} ** with you list provided and here is how to make it: \n{instructions}')
    print(f'user input was {ingredients}')
    print(f'the site :{url} was used')


# dispatchers for the various commands and listeners from within the telegram bot
dispatcher.add_handler(CommandHandler('Start', start))
dispatcher.add_handler(CommandHandler('Help', helper))


dispatcher.add_handler(MessageHandler(Filters.photo, process_photo))
dispatcher.add_handler(MessageHandler(Filters.text, get_responce))

# starting the telegram bot instance and wating for the commands

updater.start_polling()
updater.idle()

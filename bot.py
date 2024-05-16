import os

import telebot
from telebot import types
import dotenv

from commands import process_text, correct_text
from generate_stats import generate_statistics, generate_user_statistics

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

# Initialize the bot with your Telegram Bot API token
bot = telebot.TeleBot(BOT_TOKEN)

user_info = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    print("start has been chosen")
    user_id = message.from_user.id
    user_info[user_id] = {'requests': 0, 'words': 0, 'errors': {}}
    bot.send_message(message.from_user.id,
                    "Hello! This bot helps you with various text-related tasks using the TextGears API. Please use "
                    "send us our text.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    print("help has been chosen")
    help_text = """
        Here are the available commands:
        /start - Get a friendly greeting from the bot.
        /statistics - Get analyses of the text.
        In case of sending text without any commands. You are just going to get a corrected version of you text.
        """

    bot.send_message(message.from_user.id, help_text)


# Function to handle inline button for statistics
@bot.message_handler(commands=['statistics'])
def handle_statistics(message):
    user_id = message.from_user.id
    if user_id in user_info:
        print(user_info[user_id])
        # Call the function to generate statistics images
        stats = generate_user_statistics(user_info[user_id])

        # Send PNGs to the user
        with open(stats['error_type_distribution'], 'rb') as error_type_img:
            bot.send_photo(message.from_user.id, error_type_img)

        with open(stats['percentage_chance_of_mistake'], 'rb') as percentage_chance_img:
            bot.send_photo(message.from_user.id, percentage_chance_img)

        # Delete PNGs from the script
        os.remove(stats['error_type_distribution'])
        os.remove(stats['percentage_chance_of_mistake'])
    else:
        bot.send_message(message.from_user.id, 'No statistics available for this user.')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print('message has been sent')
    user_id = message.from_user.id
    user_message = message.text

    # Check if user_id exists in user_info, if not, initialize it with default values
    if user_id not in user_info:
        user_info[user_id] = {'requests': 0, 'words': 0, 'errors': {}}

    user_info[user_id]['requests'] += 1
    user_info[user_id]['words'] += len(user_message.split())
    # Pass the message to the command processing function
    response = process_text(user_message, API_KEY)
    corrected_input = correct_text(user_message, API_KEY)
    bot.send_message(message.from_user.id, corrected_input)

    # Generate statistics and plot distribution after every message
    stats = generate_statistics(response, user_message, user_info[user_id])

    # Send PNGs to the user
    with open(stats['error_type_distribution'], 'rb') as error_type_img:
        bot.send_photo(message.from_user.id, error_type_img)

    with open(stats['percentage_chance_of_mistake'], 'rb') as percentage_chance_img:
        bot.send_photo(message.from_user.id, percentage_chance_img)

    # Delete PNGs from the script
    os.remove(stats['error_type_distribution'])
    os.remove(stats['percentage_chance_of_mistake'])

    print(user_info)


# Start the bot
bot.polling()

import os
import telebot
import dotenv
from handlers.commands import process_text, correct_text
from stats.generate_stats import generate_statistics, generate_user_statistics

# Load environment variables from .env file
dotenv.load_dotenv()

# Get bot token and API key from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

# Initialize the bot with Telegram Bot API token
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store user information
user_info = {}

# Handler for '/start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Initialize user info

    user_id = message.from_user.id
    if user_id not in user_info:
        user_info[user_id] = {'requests': 0, 'words': 0, 'errors': {}}
    # Send greeting message
    bot.send_message(message.from_user.id,
                     "Hello! This bot helps you with various writing-related task. Please send us your text.")

    print(user_info)

# Handler for '/help' command
@bot.message_handler(commands=['help'])
def handle_help(message):
    # Send help text
    help_text = """
   Here are the available commands:
   /start - Get a friendly greeting from the bot.
   /statistics - Get analysis of the text.
   In case of sending text without any commands. You are just going to get a corrected version of you text.
   """
    bot.send_message(message.from_user.id, help_text)

# Handler for '/statistics' command
@bot.message_handler(commands=['statistics'])
def handle_statistics(message):
    # Generate and send statistics images to the user
    user_id = message.from_user.id
    if user_id in user_info:
        if user_info[user_id]['requests'] == 0 or len(user_info[user_id]['errors']) == 0:
            bot.send_message(message.from_user.id, "Sorry, but no record has been found for this user.")
        else:
            stats = generate_user_statistics(user_info[user_id])
            try:
                with open(stats['user_statistics'], 'rb') as user_statistics_img:
                    bot.send_photo(message.from_user.id, user_statistics_img)
                with open(stats['error_type_distribution'], 'rb') as error_type_img:
                    bot.send_photo(message.from_user.id, error_type_img)
                with open(stats['errors_per_sentence_and_word'], 'rb') as percentage_chance_img:
                    bot.send_photo(message.from_user.id, percentage_chance_img)
                os.remove(stats['user_statistics'])
                os.remove(stats['error_type_distribution'])
                os.remove(stats['errors_per_sentence_and_word.png'])
            except Exception as e:
                print(f"Error occurred: {str(e)}")

# Handler for messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_message = message.text

    # Check if user info exists, if not, initialize it
    if user_id not in user_info:
        user_info[user_id] = {'requests': 0, 'words': 0, 'errors': {}}

    # Update user info
    user_info[user_id]['requests'] += 1
    user_info[user_id]['words'] += len(user_message.split())

    # Process user message
    response = process_text(user_message, API_KEY)

    if len(response['errors']) > 0:
        corrected_input = correct_text(user_message, API_KEY)
        bot.send_message(message.from_user.id, corrected_input)
        stats = generate_statistics(response, user_message, user_info[user_id])
        try:
            with open(stats['error_type_distribution'], 'rb') as error_type_img:
                bot.send_photo(message.from_user.id, error_type_img)
            with open(stats['errors_per_sentence_and_word'], 'rb') as percentage_chance_img:
                bot.send_photo(message.from_user.id, percentage_chance_img)
            os.remove(stats['error_type_distribution'])
            os.remove(stats['errors_per_sentence_and_word'])
        except Exception as e:
            print( f"Error occurred: {str(e)}")
    else:
        msg = "No errors found in the text"
        bot.send_message(message.from_user.id, msg)

# Start the bot
bot.polling()

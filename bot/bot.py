import telebot
from commands import process_text, correct_text
# from generate_stats import generate_statistics, plot_command_distribution

TOKEN = "7043770791:AAEaF-HbtEsMsYzxXyTM_oeoSpRUyQQG6lQ"

# Initialize the bot with your Telegram Bot API token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.from_user.id, "Hello! This bot helps you with various text-related tasks using the TextGears API. Please use send us our text.")

# @bot.message_handler(commands=['help'])
#def handle_help(message):
#    help_text = """
#    Here are the available commands:
#    /start - Get a friendly greeting from the bot.
#
#    In case of sending text without any commands. You are just going to get a corrected version of you text.
#    """
#    bot.send_message(message.from_user.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    # Pass the message to the command processing function
    response = process_texts(message.text) #
    corrected_input = correct_text(message.text)
    bot.send_message(message.from_user.id, corrected_input)

    # Generate statistics and plot distribution after every message
    stats = generate_statistics(response, message.text)
    plot_command_distribution(stats['command_counts'])
    # Send the generated image back to the user
    with open('command_distribution.png', 'rb') as img:
        bot.send_photo(message.chat.id, img)

# Start the bot
bot.polling()

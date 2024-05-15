import telebot
from commands import process_command
# from generate_stats import generate_statistics, plot_command_distribution

TOKEN = "7043770791:AAEaF-HbtEsMsYzxXyTM_oeoSpRUyQQG6lQ"

# Initialize the bot with your Telegram Bot API token
bot = telebot.TeleBot(TOKEN)

messages = []  # List to store incoming messages

@bot.message_handler(commands=['hello'])
def handle_hello(message):
    bot.send_message(message.from_user.id, "Hello! This bot helps you with various text-related tasks using the TextGears API. Please use /help command to find more about our available commands")

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = """
    Here are the available commands:
    /hello - Get a friendly greeting from the bot.
    /help - Get a list of available commands and their descriptions.
    /grammar <text> - Check the grammar of the provided text.
    /spell <text> - Check the spelling of the provided text.
    /analyze <text> - Analyze the provided text.
    """
    bot.send_message(message.from_user.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    # Pass the message to the command processing function
    response = process_command(message.text)
    bot.send_message(message.from_user.id, response)

    # Generate statistics and plot distribution after every message
    # stats = generate_statistics(messages)
    # plot_command_distribution(stats['command_counts'])
    # Send the generated image back to the user
    # with open('command_distribution.png', 'rb') as img:
    #    bot.send_photo(message.chat.id, img)

# Start the bot
bot.polling()

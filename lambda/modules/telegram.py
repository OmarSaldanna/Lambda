import telebot


class Bot:

    def __init__ (self, token, chat_id):
        # set the telegram bot
        self.bot = telebot.TeleBot(token)

        # the group id "-846300715"
        self.chat_id = chat_id

        print("[TELEGRAM] -> bot controller ready")


    # Define the function to send the message
    def __call__ (self, msg):
        self.bot.send_message(self.chat_id, msg)
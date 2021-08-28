from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from config import Info
class InfoHandler():
    def __init__(self, info:Info):
        self.information = info
        self.handler = CommandHandler('info', self.info)
            
    def get_handler(self) -> Dispatcher:
        return self.handler

    def cancel(self, update: Update, context: CallbackContext) -> None:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()

    def info(self, update: Update, context: CallbackContext) -> None:
        text = f"담당교수:{self.information.PROFESSOR_NAME}\n메일주소:{self.information.CONTACT_EMAIL}\n전화번호:{self.information.CONTACT_OFFICE}\n"
        update.message.reply_text(text)
from telegram import Update
from telegram.ext import  Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

import pygsheets

from init_handler import InitHandler
from register_handler import RegisterHandler
from info_handler import InfoHandler
from score_handler import ScoreHandler

from config import TELEGRAM_API_KEY, GOOGLE_SERVICE_KEY, GOOGLE_SPREAD_SHEET, CourseInfo
from definitions import STATES

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class TutorBot():
    def __init__(self, telegram_states:list, telegram_key:str, google_service_key:str, sheet_name:str) -> None:
        # External Libraries
        # Related to pygsheets
        self.gc = pygsheets.authorize(service_file=google_service_key)
        self.sh = self.gc.open_by_key(sheet_name)
        
        # Related to python-telegram-bot
        self.updater = Updater(telegram_key)
        dp = self.updater.dispatcher

        # Internal usages
        self.state_map = {state:idx for idx, state in enumerate(telegram_states)}
        self.handlers = [
                         InitHandler(self.state_map, self.sh),
                         RegisterHandler(self.state_map, self.sh),
                         InfoHandler(CourseInfo()),]

        for content in CourseInfo.SCORE_CONTENTS:
            self.handlers.append(ScoreHandler(self.state_map, self.sh, content))
        
        for handler in self.handlers:
            dp.add_handler(handler.get_handler())
        
        dp.add_handler(CommandHandler('start', self.start))

        pass

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        context.user_data.clear()

        resp = ""
        for handler in self.handlers:
            resp += handler.get_help()
            resp += "\n"

        update.message.reply_text(resp)    
        

    def execute(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    tb = TutorBot(STATES, TELEGRAM_API_KEY, GOOGLE_SERVICE_KEY, GOOGLE_SPREAD_SHEET)
    tb.execute()


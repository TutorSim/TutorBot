from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from pygsheets import Spreadsheet

class InitHandler():
    def __init__(self,state_map:dict, sh:Spreadsheet, dp:Dispatcher):
        self.state_map = state_map
        self.sh = sh

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('init', self.handle_init_password)],
            states={
                self.state_map["GET_STUDENT_ID"]: [
                    MessageHandler(
                        Filters.regex(r'\d{5}'), self.handle_change_password
                    ),
                    MessageHandler(Filters.text & ~Filters.regex(r'\d{5}'), self.handle_unwanted_data),
                ],
                self.state_map["GET_NEW_PWD"]: [
                    MessageHandler(
                        Filters.text & ~(Filters.command), self.handle_register_password
                    )
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )

        dp.add_handler(conv_handler)
    
    def cancel(update: Update, context: CallbackContext) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        return ConversationHandler.END

    def handle_unwanted_data(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("다시 입력해주세요.")
        return self.state_map[context.user_data['next_state']]
    
    def handle_init_password(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("학번을 입력해주세요.")
        context.user_data['next_state'] = "GET_STUDENT_ID"
        return self.state_map[context.user_data['next_state']]

    def check_valid_user(self, user_id:int) -> bool:
        wks = self.sh.worksheet('title','password')
        df = wks.get_as_df()

        user_data = df.index[df['id'] == user_id].tolist()
        if user_data:
            return user_data[0]
        else:
            return -1

    def handle_change_password(self, update: Update, context: CallbackContext) -> int:
        user_id = int(update.message.text)
        if (row := self.check_valid_user(user_id)) > 0:
            context.user_data['id'] = user_id        
            context.user_data['row'] = row
            context.user_data['next_state'] = "GET_NEW_PWD"

            update.message.reply_text("변경할 비밀번호를 입력해주세요. \n평소에 사용하는 비밀번호를 사용하면 안됩니다.\n비밀번호를 공유할 경우 발생하는 문제는 개인책임입니다.")
            return self.state_map[context.user_data['next_state']]
        else:
            update.message.reply_text("수강신청 등록이 안된 사용자입니다.\n담당교수님께 확인하시길 바랍니다.")
            return ConversationHandler.END

    def handle_register_password(self, update: Update, context: CallbackContext) -> int:
        wks = self.sh.worksheet('title','password')
        wks.update_value('D'+str(context.user_data['row']+2), update.message.text)
        
        update.message.reply_text("새로운 비밀번호가 등록되었습니다.\n사용자등록을 해주시길 바랍니다.")
        
        context.user_data.clear()
        return ConversationHandler.END
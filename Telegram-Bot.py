from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup , ReplyKeyboardMarkup 
from telegram.ext import MessageHandler ,Filters , ConversationHandler
import logging
import datetime

#log file 
logging.basicConfig(format=' (asctime)s - (levelname)s - (message)s', filename='/tmp/myapp.log',filemode='a')
logger = logging.getLogger(__name__)

USERNAME , PHONE  , DOWN , DESCRIB , MAIN  = range(5)

username = ""
phone = ""
type_=""
filedownload = ""
describtion = ""


#########################    menu    #######################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('startbot', callback_data='startbot')],
              [InlineKeyboardButton('help', callback_data='help')],
              [InlineKeyboardButton('website', callback_data='website')]]
  return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard2():
  keyboard = [[InlineKeyboardButton('startbot', callback_data='startbot')],
              [InlineKeyboardButton('help', callback_data='help')]]
  return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard3():
  keyboard = [[InlineKeyboardButton('startbot', callback_data='startbot')],
             [InlineKeyboardButton('website', callback_data='website')]]
  return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard4():
    keyboard=[ ["/video"] , ["/picture"]]    
    reply_markup=ReplyKeyboardMarkup(keyboard , one_time_keyboard=True )       
    return reply_markup 

def startcon(bot, update):
  update.message.reply_text(main_menu_message(),reply_markup=main_menu_keyboard())
  

def main_menu_message(): 
    return "wellcome to my Robot.Press website or help to see information"   


def start_menu(bot, update):
  query = update.callback_query
  bot.sendMessage(text="Press 'YES' to continue .",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=ReplyKeyboardMarkup([["/yes"]] , one_time_keyboard=True ))

def help_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(text="Your Help text",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=main_menu_keyboard3())
  
  
def website_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(text="Url of your site",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        reply_markup=main_menu_keyboard2())
  
############################     functions    ########################  
def start (bot , update) :
    update.message.reply_text(text="Your name")
    return USERNAME

def username(bot, update) :
    global username
    user = update.message.from_user
    username = update.message.text
    update.message.reply_text ( "Mrs/Mr {}/ enter a cellnumber ".format(username))
    return PHONE

def phone (bot , update) :
    global phone
    user = update.message.from_user
    phone = update.message.text
    update.message.reply_text ("Upload a image or videos")
    return DOWN
    

def filedownload (bot , update) :
    global filedownload
    user = update.message.from_user
    
    try :
        filedownload =bot.get_file(update.message.photo[-1].file_id)
        filedownload.download(str(username)+"-"+str(datetime.datetime.now())+".jpg")
        update.message.reply_text ("Description for image or videos")
        return DESCRIB
    except :
        filedownload =bot.get_file(update.message.video.file_id)
        filedownload.download(str(username)+"-"+str(datetime.datetime.now())+".mp4")
        update.message.reply_text ("Description for image or videos")
        return DESCRIB
    else :
        pass
    

def describtion (bot , update) :
    global describtion
    global username
    global phone
    global filetype
    global filedownload
    user = update.message.from_user
    describtion = update.message.text
    update.message.reply_text ("Created by Masoud Taee .\n Tel : +989125573688 .\
                               \n Mail : MMTAEE64@Gmail.com")
    
    sharh = open (str(username)+"-"+str(phone)+".txt" , "a" , encoding="UTF-8")
    kamel = ("\n"+str(username)+"\n"+str(phone)+"\n"+str(describtion)+"\n"+str(datetime.datetime.now())+"\n") 
    sharh.write(kamel)
    sharh.close()
    return ConversationHandler.END

def cancel (bot , update) :
        user = update.message.from_user
        logger.info("Cancel")
        update.message.reply_text ("Cancel/Goodbye")
        return ConversationHandler.END

    
def error (bot ,update , error) :
    logger.warning ('update "%s" cause error "%s" ' , update , error)
    
    
def main () :
    updater = Updater ('Your Token here')
    dp = updater.dispatcher 
    dp.add_handler(CommandHandler('start', startcon))
    dp.add_handler(CallbackQueryHandler(start_menu, pattern='startbot'))
    dp.add_handler(CallbackQueryHandler(help_menu, pattern='help'))
    dp.add_handler(CallbackQueryHandler(website_menu, pattern='website'))
   
    con_handler = ConversationHandler(
            entry_points=[CommandHandler("yes",start)],
            states={
                    USERNAME : [MessageHandler(Filters.text,username)] ,
                    PHONE    : [MessageHandler(Filters.text,phone)] ,
                    DOWN     : [MessageHandler(Filters.all,filedownload)] , 
                    DESCRIB  : [MessageHandler(Filters.text,describtion)] ,
                    },
            fallbacks=[CommandHandler("cancel",cancel)]  
            )

    dp.add_handler(con_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()  


if __name__ == "__main__" : 
  main()

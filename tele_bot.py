from email.policy import default
import imp
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
import pymongo
# from utils import validate,sensorReading


client = pymongo.MongoClient("mongodb+srv://harshnishad:harshnishad@cluster0.llahgwx.mongodb.net/test")
db = client["tele_id"]
keys=db["keys"]


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg="Now you will get alerts when the sensor is faulty"
    print(update.effective_chat.id)
    keys.insert_one({"chat_id":update.effective_chat.id})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)



# async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     msg=""
#     if(len(context.args)==0):
#         msg="Invalid format\nType in given format\n\n/register username password"
#     else:
#         username=context.args[0]
#         password=context.args[1]
#         msg=validate(username,password,update.effective_chat.id)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

# async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     readings=sensorReading(update.effective_chat.id)
#     await context.bot.send_message(chat_id=update.effective_chat.id)



    

if __name__ == '__main__':
    TOKEN = "6184416177:AAGzElvMve5KnyiCEh7l9b3Plh526ILkrL0"
    application = ApplicationBuilder().token(TOKEN).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    # register_handler = CommandHandler('register', register)
    # status_handler = CommandHandler('status', status)

    application.add_handler(start_handler)
    # application.add_handler(status_handler)
    # application.add_handler(register_handler)
    application.add_handler(echo_handler)
    

    application.run_polling()

    application.run_polling()

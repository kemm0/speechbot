from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging
import voicesynth
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
updater = Updater(BOT_TOKEN)

dispatcher = updater.dispatcher

print("Bot started polling")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO,filename="debug.log")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def sano(update,context):
    text = update.message.text
    filtered = text.replace('/sano ', '')
    file_path = voicesynth.get_audio(filtered,'message','./generated','./sounds')

    time_to_wait = 5
    time_counter = 0
    file_ready = False

    if os.path.exists(file_path):
      file_ready = True
    
    while not os.path.exists(file_path):
      time.sleep(1)
      time_counter += 1
      if os.path.exists(file_path):
        file_ready = True
        break
      if time_counter > time_to_wait:
        break
    if file_ready:
      logging.log(level=logging.INFO,msg="Created file {}".format(file_path))
      try:
        context.bot.send_voice(chat_id=update.effective_chat.id,voice=open(file_path,'rb'))
        os.remove(file_path)
      except TimedOut:
        logging.log(level=logging.ERROR,msg="Timed out")
      except e:
        logging.log(level=logging.ERROR,msg=e)
    else:
      context.bot.send_message(chat_id=update.effective_chat.id, text='failed to send speech :(')

speech_handler = CommandHandler('sano',sano)

dispatcher.add_handler(speech_handler)


updater.start_polling()
updater.idle()

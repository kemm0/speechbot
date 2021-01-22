from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging
import voicesynth
import time
from dotenv import load_dotenv
import random

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
updater = Updater(BOT_TOKEN)

dispatcher = updater.dispatcher

print("Bot started polling")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

viisaudet = []
ennustukset = []

def load_viisaudet(path):
  viisaudet_file = open(path,'r')
  for line in viisaudet_file:
    viisaudet.append(line)
  print("viisaudet loaded")
  print(len(viisaudet))

def load_ennustukset(path):
  ennustukset_file = open(path,'r')
  for line in ennustukset_file:
    ennustukset.append(line)
  print("ennustukset loaded")
  print(len(ennustukset))

def echo(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def viisaus(update, context):
  i = random.randrange(len(viisaudet))
  rand_viisaus = viisaudet[i]
  file_path = voicesynth.get_audio(rand_viisaus,'viisaus','./generated','./resources/sounds')
  send_file(update, context, file_path)

def ennustus(update, context):
  i = random.randrange(len(ennustukset))
  rand_ennustus = ennustukset[i]
  file_path = voicesynth.get_audio(rand_ennustus,'ennustus','./generated','./resources/sounds')
  send_file(update, context, file_path)

def sano(update,context):
  print(update.message.text)
  text = update.message.text
  filtered = text.replace('/sano ', '')
  file_path = voicesynth.get_audio(filtered,'message','./generated','./resources/sounds')
  send_file(update,context,file_path)

def send_file(update,context,file_path):
  print(update.message.text)
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
    print("file ready")
    logging.log(level=logging.INFO,msg="Created file {}".format(file_path))
    try:
      context.bot.send_voice(chat_id=update.effective_chat.id,voice=open(file_path,'rb'))
      os.remove(file_path)
    except e:
      print(e)
      logging.log(level=logging.ERROR,msg=e)
  else:
    context.bot.send_message(chat_id=update.effective_chat.id, text='failed to send speech :(')


load_viisaudet('./resources/viisaudet.txt')
load_ennustukset('./resources/ennustus.txt')

speech_handler = CommandHandler('sano',sano)
viisaus_handler = CommandHandler('viisaus',viisaus)
ennustus_handler = CommandHandler('horoskooppi', ennustus)
dispatcher.add_handler(speech_handler)
dispatcher.add_handler(viisaus_handler)
dispatcher.add_handler(ennustus_handler)

updater.start_polling()
updater.idle()

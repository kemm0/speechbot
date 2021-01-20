import wave
import sys
import os
import string
import random

def get_random_id(max):
  id = random.randint(1, max + 1)
  return id

def createaudio(filename,dest,dir,files):

  data= []
  for file in files:
      w = wave.open("{}/{}".format(dir,file), 'rb')
      data.append( [w.getparams(), w.readframes(w.getnframes())] )
      w.close()
  file_path = "{}/{}".format(dest,filename)
  output = wave.open(file_path, 'wb')
  output.setparams(data[0][0])
  for i in range(len(data)):
      output.writeframes(data[i][1])
  output.close()
  return file_path

def map_sounds(dir):

  sounds = os.listdir(dir)
  sound_alphabet_mapping = {}

  for sound_file in sounds:
    sound_name = sound_file[:-4]
    if(sound_name == 'space'):
      sound_alphabet_mapping[' '] = sound_file

    elif(sound_name == 'dot'):
      sound_alphabet_mapping['.'] = sound_file
      sound_alphabet_mapping['!'] = sound_file
      sound_alphabet_mapping['?'] = sound_file

    else:
      sound_alphabet_mapping[sound_name] = sound_file

  return sound_alphabet_mapping

def get_audio_content(text,audio_mapping):
  text = text.lower()
  audio_files = []
  i=0
  while(i < len(text)):

    if(i+1 < len(text)):

      if(text[i] == text[i+1]):
        syllable = text[i] + text[i+1]

        if(syllable in audio_mapping):
          soundfile = audio_mapping[syllable]
          audio_files.append(soundfile)
          i += 2
          continue
    character = text[i]
    if(character in audio_mapping):
      soundfile = audio_mapping[character]
      audio_files.append(soundfile)
    i += 1

  return audio_files

def get_audio(text,filename,dest_dir,sounds_lib_dir,id_max=100):

  sounds = map_sounds(sounds_lib_dir)
  audio_files = get_audio_content(text,sounds)
  file_id = "{}{}.wav".format(filename,get_random_id(id_max))
  ids = os.listdir(dest_dir)
  while(file_id in ids):
    file_id = "{}{}.wav".format(filename,get_random_id(id_max))

  file_path = createaudio(file_id,dest_dir,sounds_lib_dir,audio_files)
  return file_path
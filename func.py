import database
import os
import requests
import json
import random

from dotenv import load_dotenv

load_dotenv()
TENOR_API = os.getenv('TENOR_API')
limit = 20

replace_char = ' .,/\\?!@#$%^&*-_=+<>()[]{}'

def trimchar(txt) -> str:
  temp = txt
  for ch in replace_char:
    temp = temp.replace(ch,'')
  return temp

def unhealthy_words(word):
  return any(words in trimchar(healthy_words(word.lower())) for words in database.answer_response_sensitive)

def healthy_words(word) -> str:
  temp = word
  for words in database.answer_response_unsensitive:
    temp = temp.replace(words,'')
  return temp

def my_add_role(mem, role):
  mem.add_role(role, None, None)

def get_gif(keyword) -> str:
  resp = requests.get(
    "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % 
    (keyword, TENOR_API, 'ckey',  limit))
  if resp.status_code == 200:
    # return the search predictions
    search_term_list = json.loads(resp.content)['results']
    gif_id = random.choice(search_term_list)['url']
    print(gif_id )
    return gif_id
  else:
    # handle a possible error
    return ''

def is_member(memID, listMember):
  print(len(listMember))
  return any(mem.id == memID for mem in listMember)
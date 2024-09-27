import random

answer_response_true = ["Hello", "Hi, there", "I'm here","You're awesome"]
answer_response_false= [('éo có','gì hết'), 
                        ('qq gì mà','lắm thế'),
                        ('suốt ngày','' ,'','')]

answer_response_sensitive = ['cặc', 'lồn', 'đụ','địtmẹ'
                              'conmẹ','thằngchó',
                              'conđĩ','pussy','địtcụ',
                              'thằngcha', 'địtmẹ', 'kặc']

answer_response_unsensitive = ['đụng', 'đục']

choice = range(0,1000)

def _response_() -> bool:
  return random.choice(choice) < 700

def rsp_tr() -> str:
  return random.choice(answer_response_true)

def rsp_f() -> tuple:
  return random.choice(answer_response_false)
  
def rsp_unsensitive():
  return any(word in answer_response_unsensitive for word in answer_response_sensitive)

def database():
  return

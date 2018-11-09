import os
import smtplib
import telepot
import telegram
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("pikkiobot@gmail.com", "Pikkiobot01")

def genFiles(mex):
	global infos
	global send
	infos = mex.split('/')
	command = 'echo ' + str(infos[0]) + '> README' 
	os.system(command)
	command = 'echo ' + str(infos[1]) + '> INSTALL'
	os.system(command)
	command = 'tar -cvzf es_' + str(fileName[0:len(fileName)-4]) + '.tar README INSTALL COPYNG ' + str(fileName)
	send = 'es_' + str(fileName[0:len(fileName)-4]) + '.tar'
	os.system(command)
	print("ZIP Completato!")

def sendMail(user):
	emailTo = str(infos[2])
	email = MIMEMultipart('alternative')
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(send, 'rb').read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachement; filename=' + str(send))
	email.attach(part)
	email["Subject"] = '@' + user + 'Pikkio Exercise'
	email["From"] = 'pikkiobot@gmail.com'
	email["To"] = emailTo
	server.sendmail('pikkiobot@gmail.com', emailTo, email.as_string())	
	print("Email Inviata! DONE")

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	global fileName

	if content_type == 'document':
		print('Download del file in corso ...')
		idFile = msg['document']['file_id']
		fileName = msg['document']['file_name']
		#TODO : Rinominare o no sempre il file in main.cpp?
		bot.download_file(idFile, fileName)
		print('File downloadato con successo!')
		#Per distinguere il testo che andra in readme/install/copyng diro di separare con uno slash e quindi .split('/')		
		bot.sendMessage(chat_id, "Ora inserisci il testo per i file di pikkio readme/install/email a cui inviare separati da <b>/</b>", parse_mode='HTML')
	if content_type == 'text':
		mex = msg['text']
		user = str(msg['from']['first_name'])
		print("Nome file : ", mex, " da utente : ", user)
		genFiles(mex)
		sendMail(user)

TOKEN = '768658931:AAEuieS0SDJfnjEX0kPDd0meHJlBryWRUT4'
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message})

import time
while 1:
    time.sleep(10)

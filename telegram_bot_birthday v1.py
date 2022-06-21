#!/usr/bin/python3

import pandas as pd
from datetime import datetime, timedelta

import telebot
import time


# сделаем ссылку на файл xlsx на гугл диске
path = 'https://docs.google.com/spreadsheets/d/13xC31I6qTzFTCFooZmkijFGiJFh7q2Ut/edit?usp=sharing&ouid=108304778138479696406&rtpof=true&sd=true'
path = 'https://drive.google.com/uc?id=' + path.split('/')[-2]


# функция преобразования файла эксель в норм датафрэйм вынесена в отдельный файл
from setup import make_df_from_xlsx
data = make_df_from_xlsx(path)


# сделаем мини датафрэймы - у кого др сегодня и у кого др завтра
data_birthday = data[data['this_year_birthday'] == datetime.strftime(datetime.today(), '%Y-%m-%d')]
data_birthday_tomorrow = data[data['this_year_birthday'] == datetime.strftime(datetime.today() + timedelta(days=1), '%Y-%m-%d')]

# также сделаем df с ближайшим др
nearest_birthday = data[data['timedelta'] == data[data['timedelta'] > 0]['timedelta'].min()]
data_birthday_soon = nearest_birthday


#  импортируем наши переменные: ключ-token и адрес канала
# У меня они выведены в отдельный файл
import keys
token = keys.token
# Адрес телеграм-канала, начинается с @ - если он публичный и с '-100' - если он приватный 
CHANNEL_NAME = keys.CHANNEL_NAME

# Создаем экземпляр бота
bot = telebot.TeleBot(token)

if data_birthday.shape[0] > 0:
  bot.send_message(CHANNEL_NAME, "Cегодняшние именниники:")
  for i in range(data_birthday.shape[0]):
    bot.send_message(CHANNEL_NAME, f" {data_birthday['employee'].iloc[i]}, \
                                      {data_birthday['organisation'].iloc[i]}, \
                                      {data_birthday['position'].iloc[i]}, \
                                      исполнилось {datetime.now().year - int(data_birthday['birthday'].iloc[i].year)}")
else:
  bot.send_message(CHANNEL_NAME, "У наших сегодня ДР нет")

if data_birthday_tomorrow.shape[0] > 0:
  bot.send_message(CHANNEL_NAME, "Дни рождения завтра:")
  for i in range(data_birthday_tomorrow.shape[0]):
    bot.send_message(CHANNEL_NAME, f" {data_birthday_tomorrow['employee'].iloc[i]}, \
                                      {data_birthday_tomorrow['organisation'].iloc[i]}, \
                                      {data_birthday_tomorrow['position'].iloc[i]}, \
                                      исполнилось {datetime.now().year - int(data_birthday_tomorrow['birthday'].iloc[i].year)}")
else:
  bot.send_message(CHANNEL_NAME, "Завтра ДР нет")
  bot.send_message(CHANNEL_NAME, f"Следующий ближайший ДР {str(data_birthday_soon.iloc[0]['this_year_birthday'])[5:11]}")
  for i in range(data_birthday_soon.shape[0]):
    bot.send_message(CHANNEL_NAME, f"{data_birthday_soon['employee'].iloc[i]}, \
                                     {data_birthday_soon['organisation'].iloc[i]},  \
                                     {data_birthday_soon['position'].iloc[i]} ")




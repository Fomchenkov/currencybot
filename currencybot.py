#!/usr/bin/python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import requests
import json


BOT_TOKEN = '387480715:AAGE4QwIkF6OaTaCln8vB4eAWPwD8Nes_fM' # Your bot TOKEN
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def cmd_start(message):
	text = "Привет!\nЯ умею определять курс валют к рублю. "
	text += "Нажми на кнопку ниже, что бы узнать курс валют."
	keyboard = types.InlineKeyboardMarkup()
	""" callback_data must be equal current id (API) """
	dollar_btn = types.InlineKeyboardButton(text="USDRUB", callback_data="USDRUB")
	euro_btn = types.InlineKeyboardButton(text="EURRUB", callback_data="EURRUB")
	keyboard.add(dollar_btn, euro_btn)
	return bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		url = "https://query.yahooapis.com/v1/public/yql?q=select+*+from+yahoo."
		url += "finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env="
		url += "store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
		data = json.loads(requests.get(url).text)

		for x in data["query"]["results"]["rate"]:
			if x["id"] == call.data:
				text = "Отношение валют: " + x["Name"] + "\n" 
				text += "Дата: " + x["Date"] + "\nВремя: " + x["Time"] + "\n\n"
				text += "Значение: <b>" + x["Rate"] + " RUB</b>"
				return bot.send_message(call.message.chat.id, text, parse_mode="html")

		return bot.send_message(call.message.chat.id, "Нет такой валюты.", parse_mode="html")


if __name__ == '__main__':
	bot.polling(none_stop=True)

# -*- coding: utf-8 -*-

import os
import json
import logging
import requests
import re
from slackclient import SlackClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
	logger.info('event: ' + json.dumps(event))

	if ('params' in event) and \
		('querystring' in event['params']) and \
		('hub.challenge' in event['params']['querystring']):
		return int(event['params']['querystring']['hub.challenge'])

	if ('object' in event) and \
		('group' in event['object']) and \
		('changes' in event['entry'][0]) and \
		(event['entry'][0]['changes'][0]['field'] == 'posts'):

		post = event['entry'][0]['changes'][0]

		group_id = event['entry'][0]['id']
		user_name = post['value']['from']['name']
		wp_link = post['value']['permalink_url']
		msg = post['value']['message']

		wp_url = 'https://graph.facebook.com/' + group_id + '?fields=name,description&access_token=' + os.environ['wp_token']
		response = requests.get(wp_url)
		data = response.json()

		logger.info('URL: ' + wp_url)
		logger.info('Response: ' + response.text)
		logger.info('parameters: ' + group_id + ', ' + user_name  + ', ' + wp_link + ', ' + msg)

		if ('description' in data):
			group_name = data['name']
			channel = getSlackChannel(data['description'])

			if channel is not None:
				logger.info('channel: ' + channel)

				message = '_BOOOOOOOOOMMMMM DIIIIAAAAAAAAAAAAAAAA!!!!!_ \n' + \
							':workplace: Novo post de *' + user_name.upper() + '* no grupo *' + group_name.upper() + '*! :workplace: \n' + \
							':point_right: :' + wp_link +  ' :point_left: \n ' + \
							' ------------------------------- \n ' + msg
				sendMessage(channel, message)

def getSlackChannel(description):
	matchObj = re.search( r'(?<=slack:).+', description , re.M|re.I )

	if matchObj:
		return matchObj.group()
	else:
		return None

# Envia uma mensagem no slack como o BOT
def sendMessage(channel, message):
	sc = SlackClient(os.environ['sl_token'])

	sc.api_call(
		"chat.postMessage",
		channel=channel,
		text=message,
		icon_emoji=':bom-diaaaa:',
		as_user='false',
		username='Elmo felizão!!!'
	)
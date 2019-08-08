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

	if 'action' in event:
		if 'summary' == event['action']:
			summary()
		if 'disturb' == event['action']:
			disturb()

def summary():
	session_token = getSessionToken()
	headers = {"App-Token" : os.environ['app_token'],"Session-Token" : session_token}

	url = os.environ['glpi_summary']

	response = requests.get(url, headers=headers, verify=False)
	data = response.json()

	logger.info('URL: ' + url)
	logger.info('Response: ' + response.text)

	openItens = 0
	lateItens = 0
	categories = {}
	for item in data['data']:
		categoryComplete = item['Ticket.ITILCategory.completename']
		openItens += 1

		if item['Ticket.is_late'] == 1:
			lateItens += 1

		if categoryComplete is not None:
			if len(categoryComplete.split('>'))>1:
				category = categoryComplete.replace(categoryComplete.split('>')[0], '', 1) 
			else:
				category = categoryComplete.split('>')

			if category in categories:
				categories[category] += 1
			else:
				categories[category] = 1

	msg = '_Hoje temos *' + str(openItens) + ' chamados abertos*, sendo *' + str(lateItens) + ' atrasados* :grimacing:_' + '\n\n'
	msg += 'Veja os tipos mais recorrentes:' + '\n'

	sorted_categories = sorted(categories, key=categories.__getitem__)
	i = 0
	for k in reversed(sorted_categories):
		msg += str(k) + ' - *' + str(categories[k]) + ' chamados*' + '\n'
		i += 1
		if i==3:
			break

	msg += '\n' + '_Vejo vocês em 7 dias...._'

	sendMessage(os.environ['sl_channel'], msg)


def disturb():
	session_token = getSessionToken()
	headers = {"App-Token" : os.environ['app_token'],"Session-Token" : session_token}

	url = os.environ['glpi_url'] + '/apirest.php/ITILCategory'
	response = requests.get(url, headers=headers, verify=False)
	data = response.json()

	logger.info('URL: ' + url)

	efforts= {}
	for item in data:
		if item['comment'] is not None:
			if item['comment'].startswith('EFFORT='):
				efforts[item['completename']] = int(item['comment'].replace('EFFORT=', ''))

	logger.info('Efforts: ' + str(efforts))

	url = os.environ['glpi_disturb']

	response = requests.get(url, headers=headers, verify=False)
	data = response.json()

	logger.info('URL: ' + url)
	logger.info('Response: ' + response.text)

	closedItems = 0
	issues = {}
	issueEffort = {}
	users = {}
	for item in data['data']:
		user = item['Ticket.Ticket_User.User.name']
		closedItems += 1

		if user is not None:
			if type(user) is list:
				user = user[0]

			effort = 1
			if 'Ticket.ITILCategory.completename' in item and item['Ticket.ITILCategory.completename'] in efforts:
				effort = 1 * efforts[item['Ticket.ITILCategory.completename']]

			if user in issueEffort:
				issueEffort[user] += effort
				issues[user] += 1
			else:
				url = os.environ['glpi_url'] + '/apirest.php/User/' + str(user)
				response = requests.get(url, headers=headers, verify=False)
				data2 = response.json()

				issueEffort[user] = effort
				issues[user] = 1
				users[user] = data2['firstname']
				
	msg = '_Nos ultimos 7 dias foram atendidos *' + str(closedItems) + ' chamados*:_' + '\n'

	sorted_categories = sorted(issueEffort, key=issueEffort.__getitem__)
	i = 0
	for k in reversed(sorted_categories):
		msg += str(users[k]) + ' - * Esforço: ' + str(issueEffort[k]) + '* em *' + str(issues[k]) + ' chamados*' + '\n'

	msg += '\n' + '_Vejo vocês em 7 dias...._'

	sendMessage(os.environ['sl_channel'], msg)



def getSessionToken():
	headers = {"App-Token" : os.environ['app_token'],"Authorization" : os.environ['authorization'],"Content-Type" : "application/json"}
	url = os.environ['glpi_url'] + '/apirest.php/initSession'

	response = requests.get(url, headers=headers, verify=False)
	data = response.json()

	logger.info('URL: ' + url)
	logger.info('Response: ' + response.text)
	return data['session_token']


# Envia uma mensagem no slack como o BOT
def sendMessage(channel, message):
	sc = SlackClient(os.environ['sl_token'])

	sc.api_call(
		"chat.postMessage",
		channel=channel,
		text=message,
		icon_emoji=':samara:',
		as_user='false',
		username='Samara'
	)
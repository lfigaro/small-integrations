import os
import json
import logging
import requests
import sys
import xmltodict
import boto3
from cmd.boardgame import boardgame

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class syncBGG:

	def __init__(self, event):
		if 'inicio' in event:
			self.inicio = event['inicio']
		else:
			self.inicio = 355000

		if 'fim' in event:
			self.fim = event['fim']
		else:
			self.fim = self.inicio + 10

		if 'lote' in event:
			self.lote = event['lote']
		else:
			self.lote = 10

		self.event = event

	def execute(self):
		url = os.environ['bgg_url'] + 'thing?type=boardgame&id='

		# para testes
		i = 0
		bgsList = []
		for n in range(self.inicio, self.fim):
			if i == self.lote:
				url = url[:-1]
				i = 0

				logger.info('BGG URL: ' + url)

				response = requests.get(url) #, auth=(os.environ['user'], os.environ['pass']), headers=headers)
				bgs = xmltodict.parse(response.text)
				#logger.info(bgs)

				table = boto3.resource('dynamodb').Table("boardgames")
				table.load()

				for bg in bgs["items"]["item"]:
					bg = self.find_name_languages(bg)

					bg['_id']=bg['@id']

					description = bg["description"]
					description_pt = self.translate_text(description)

					bg['description'] = [
						{"language":"pt", "text":description_pt},
						{"language":"en", "text":description}]
					bgsList.append(bg)
					#logger.info(bg)
				
				boardgameclass = boardgame(event=self.event)
				ret = boardgameclass.set_boardgames(bgsList)

				if ret.status_code >= 200 and  ret.status_code <= 299:
					logger.info('boardgames added: ' + str(ret.status_code) + ' - ' + str(ret.json()['insertedIds']))
				else:
					logger.error('set_boardgame response error: ' + str(ret.status_code) + ' - ' + ret.text)

				url = os.environ['bgg_url'] + 'thing?type=boardgame&id='
				bgsList = []

			url += (str(n) + ',')
			i+=1
		return

	def split_by_n(self, seq, n):
		while seq:
			yield seq[:n]
			seq = seq[n:]

	def translate_text(self, text):
		if len(text) > 2000:
			text = self.split_by_n(text, 2000)
			ret = ''
			for t in text:
				response = requests.post(os.environ['translate_url'] + "translate", 
					headers = { "Content-Type": "application/json" }, 
					json = {
						"q": t,
						"source": "en",
						"target": "pt",
						"format": "text",
						"api_key": os.environ['translate_key']
					}
				)
				ret+=(response.json()['translatedText'])

		else:
			response = requests.post(os.environ['translate_url'] + "translate", 
				headers = { "Content-Type": "application/json" }, 
				json = {
					"q": text,
					"source": "en",
					"target": "pt",
					"format": "text",
					"api_key": os.environ['translate_key']
				}
			)
			
			ret = response.json()['translatedText']

		return(ret)

	def find_language(self, name):
		response = requests.post(os.environ['translate_url'] + "detect", 
			headers = { "Content-Type": "application/json" }, 
			json = {
				"q": name['@value'],
				"api_key": os.environ['translate_key']
			}
		)

		name['language'] = response.json()[0]['language']
		return name

	def find_name_languages(self, bg):
		#logger.info(bg)
		name = bg["name"]
		if isinstance(name, dict):
			bg['name'] = self.find_language(name)

		if isinstance(name, list):
			temp = []
			for n in name:
				temp.append(self.find_language(n))
			bg['name'] = temp

		return bg

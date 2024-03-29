import os
import json
import logging
import requests
import sys
import xmltodict
import boto3

from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class boardgame:
	def __init__(self, event):
		self.table = boto3.resource('dynamodb').Table("boardgames")
		self.event = event
		self.headers = {
		  'Content-Type': 'application/json',
		  'Access-Control-Request-Headers': '*',
		  'api-key': os.environ['mongo_db_access_key']
		}
		self.mongo_db_url=os.environ['mongo_db_url']

	def execute(self):
		logger.info('event: ' + str(self.event))
		if 'action' in self.event and self.event['action'] is not None:
			ret = None

			if self.event['action'] == "get_boardgame":
				objectid = self.event['objectid']
				ret = self.get_boardgame(objectid)
				return json.dumps(ret)

	def get_boardgame_dynamodb(self, objectid):
		client = boto3.client('dynamodb')
		response = client.get_item(TableName='boardgames', Key={'@objectid':{'S': objectid}})
		return self.unmarshal_response(response['Item'])

	def get_boardgame(self, objectid):
		payload = json.dumps({
		    "collection": "boardgames",
		    "database": "boardgameplay",
		    "dataSource": "Cluster0"
		})
		response = requests.request("POST", 
			self.mongo_db_url + 'findOne', 
			headers=self.headers, 
			data=payload)
		return response.json()

	def set_boardgame(self, bg):
			payload = json.dumps({
			    "collection": "boardgames",
			    "database": "boardgameplay",
			    "dataSource": "Cluster0",
			    "document": bg
			})
			response = requests.request("POST", 
				self.mongo_db_url + 'insertOne', 
				headers=self.headers, 
				data=payload)
			return response

	def set_boardgames(self, bgs):
			payload = json.dumps({
			    "collection": "boardgames",
			    "database": "boardgameplay",
			    "dataSource": "Cluster0",
			    "documents": bgs
			})
			response = requests.request("POST", 
				self.mongo_db_url + 'insertMany', 
				headers=self.headers, 
				data=payload)
			return response

import importlib
import requests
import json
import logging
import os
import sys
import base64

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
	logger.info('event: ' + json.dumps(event))

	# Get from POST or GET requests
	if 'body' in event and \
	   event['body'] is not None:
		
		evnt = base64.b64decode(event['body']).decode('utf-8')
		temp = {}
		for params in evnt.split("&"):
			param = params.split("=")
			temp[param[0]] = param[1]
		event = temp
		logger.info('event: ' + str(event))

	elif 'queryStringParameters' in event and \
	   event['queryStringParameters'] is not None:
		event = event['queryStringParameters']
		logger.info('event: ' + str(event))

	# Comandos
	if 'command' in event and event['command'] is not None:
		logger.info('command: ' + event['command'] + ' - ' + json.dumps(event))
		class_ = getattr(importlib.import_module("cmd." + event['command']), event['command'])
		command = class_(event)
		ret = command.execute()

		#logger.info('return: ' + str(ret))

		return ret


# To execute by command line
if __name__ == "__main__":
	logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
	args = ''
	for index in range(len(sys.argv)):
		if index > 0:
			args += sys.argv[index] + ' '

	logger.info('args: ' + args)
	lambda_handler (json.loads(args), None)
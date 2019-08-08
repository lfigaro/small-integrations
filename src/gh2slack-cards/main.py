# -*- coding: utf-8 -*-

import os
import json
import logging
import requests
import re
import sys
from slackclient import SlackClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    ret = 'Hello World!'

    try:

        if ('body' in event):
            event = json.loads(event['body'])

        if ('zen' in event):
            return {
                "statusCode": 200,
                "isBase64Encoded": False,
                'body': event['zen']
            }

        logger.info('event: ' + json.dumps(event))

        if ('action' in event) and \
           ((event['action'] == 'created') or (event['action'] == 'converted')) and \
           ('project_card' in event):

            url = event['project_card']['content_url']
            headers = {"Accept" : "application/vnd.github.inertia-preview+json"}
            logger.info('GitHub URL: ' + url)
            response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
            logger.info('GitHub Response: ' + response.text)
            issue = response.json()

            url = event['project_card']['project_url']
            headers = {"Accept" : "application/vnd.github.inertia-preview+json"}
            logger.info('GitHub URL: ' + url)
            response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
            logger.info('GitHub Response: ' + response.text)

            project = response.json()
            channel = getSlackChannel(project['body'])

            if (channel is not None):
                message = 'Novos cards :spades::hearts::clubs::diamonds: incluídos em *' + project['name'] + '* \n'
                message += '> *' + issue['title'] + '* \n'
                message += '> _' + issue['body'] + '_ \n'
                message += '[' + issue['html_url'] + '] \n'

                sendMessage(channel, message)

    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        return {
            "statusCode": 500,
            "isBase64Encoded": False,
            'body': repr(e)
        }

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        'body': ret
    }

# Recupera o canal do slack
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
        icon_emoji=':croupier:',
        as_user='false',
        username='Croupier'
    )
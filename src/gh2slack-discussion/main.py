# -*- coding: utf-8 -*-

import os
import json
import logging
import requests
from slackclient import SlackClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

teamsList = []

def processTeamDiscussion( team ):
    logger.info('Starting team: ' + team['name'])

    if team['name'] not in teamsList:
        teamName = team['name']
        teamsList.append(teamName)

        url = 'https://api.github.com/teams/' + str(team['id']) + '/discussions'
        headers = {"Accept" : "application/vnd.github.echo-preview+json"}
        logger.info('GitHub URL: ' + url)
        response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
        logger.info('GitHub URL: ' + response.text)

        msg = "Discussões abertas atualmente no time: *" + team['name'] + "*\n\n"
        hasDiscussions = False
        data2 = response.json()
        for discussion in data2:
            if not discussion['title'].upper().startswith('[CLOSED]'):
                msg = msg + '*' + discussion['title'] + '.*  ' + discussion['html_url'] + '\n'
                hasDiscussions = True

        msg = msg + "\n\n PS.: Para fechar uma discussão é só colocar a tag _[CLOSED]_ no início do título :-)"
        
        # Comente essa linha para subir em prod
        # teamName = "teste-zavi" 

        if hasDiscussions:
            sc = SlackClient(os.environ['sl_token'])

            sc.api_call(
              "chat.postMessage",
              channel=teamName,
              text=msg,
              icon_emoji=':speech_balloon:',
              as_user='false',
              username='O que tá rolando?'
            )
    return

def handler(event, context):
    url = 'https://api.github.com/orgs/' + str(os.environ['org']) + '/teams'
    headers = {"Accept" : "application/vnd.github.hellcat-preview+json"}
    
    logger.info('GitHub URL: ' + url)
    response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
    logger.info('GitHub Response: ' + response.text)

    data = response.json()
    for team in data:
        processTeamDiscussion(team)

        if ('parent' in team) and (team['parent'] is not None):
            processTeamDiscussion(team['parent'])

    return 'Hello World'
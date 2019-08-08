import os
import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    
    logger.info('got event{}: ' + json.dumps(event))
    if (('action' in event) and 
        ('content_url' in event['project_card']) and 
        (event['action'] == 'moved') or 
        (event['action'] == 'converted') or 
        (event['action'] == 'created')):

        # Consulta o nome da coluna
        url = event['project_card']['column_url']
        issue_url=event['project_card']['content_url']
        headers = {"Accept" : "application/vnd.github.inertia-preview+json"}
        
        logger.info('GitHub URL: ' + url)
        response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
        logger.info('GitHub Response: ' + response.text)

        column = response.json()
        state = column['name']
        project_url = column['project_url']

        response = requests.get(project_url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
        logger.info('GitHub Response: ' + response.text)

        project = response.json()
        project_name = project['name']

        if not project_name.startswith('#'):
            if state.lower() == 'done':
                data = {'state': 'closed'}

                response = requests.post(issue_url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                logger.info('GitHub Response: ' + response.text)

    return 'Hello World'

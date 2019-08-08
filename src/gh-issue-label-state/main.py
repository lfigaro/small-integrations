import os
import json
import logging
import requests
import sys

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
    
        logger.info('got event{}: ' + json.dumps(event))
        if (('action' in event) and 
            ('content_url' in event['project_card']) and 
            (event['action'] == 'moved') or 
            (event['action'] == 'converted') or 
            (event['action'] == 'created')):

            # Consulta o nome da coluna
            url = event['project_card']['column_url']
            headers = {"Accept" : "application/vnd.github.inertia-preview+json"}
            
            logger.info('GitHub URL: ' + url)
            response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
            logger.info('GitHub Response: ' + response.text)

            column = response.json()
            state = column['name']
            project_url = column['project_url']
            stateName = 'state/'+state.replace(' ', '-').lower()

            logger.info('GitHub URL: ' + project_url)
            response = requests.get(project_url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
            logger.info('GitHub Response: ' + response.text)

            project = response.json()
            project_name = project['name']

            if not project_name.startswith('#'):
                url = event['project_card']['content_url']
                
                logger.info('GitHub URL: ' + url)
                response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
                logger.info('GitHub Response: ' + response.text)

                issue = response.json()
                label = None
                labels = []
                for labelTemp in issue['labels']:
                    if not labelTemp['name'].startswith('state/'):
                        labels.append(labelTemp)
                labels.append(stateName)
                data = {'labels' : labels}

                response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                logger.info('GitHub Response: ' + response.text)

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

import os
import json
import logging
import requests
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    repos = os.environ['repos'].split(',')
    for repo in repos:
        count_vote('https://api.github.com/repos/' + repo + '/issues?state=open&per_page=500')
    return

def count_vote(url):
    headers = {"Accept" : "application/vnd.github.squirrel-girl-preview"}
    
    while url is not None:
        logger.info('GitHub URL: ' + url)
        response = requests.get(url, auth=(os.environ['user'], os.environ['pass']), headers=headers)
        logger.info('List Issue Response: ' + response.text)

        link = response.headers.get('link', None)
        data = response.json()
        for issue in data:
            if 'pull_request' not in issue:
                votes = issue['reactions']['+1']
                labels = []
                
                for labelTemp in issue['labels']:
                    if not labelTemp['name'].startswith('votes/'):
                        labels.append(labelTemp)
                
                labels.append('votes/' + str(votes))
                data = {#'title': issue['title'],
                        'labels': labels}

                headers = {"Accept" : "application/vnd.github.symmetra-preview+json"}
                response = requests.patch(issue['url'], json.dumps(data), auth=(os.environ['user'], os.environ['pass']), headers=headers)
                logger.info('Issue Response: ' + response.text)

        if link is not None:
            url = next_page(link)
        else:
            url = None

    return


def next_page(link):
    matchObj = re.search( r'\<[^<]*?\>; rel="next"', link , re.M|re.I )
    
    if matchObj:
        return matchObj.group().replace('<','').replace('>; rel="next"','')
    else:
        return None

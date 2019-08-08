import os
import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info('got event{}: ' + json.dumps(event))
    issue = event['issue']
    repository = event['repository']
    
    # Retorna o primeiro nome do autor da alteracao
    sender = event['sender']
    senderLogin = sender['login']
    
    # Busca o repositorio pelo id do projeto
    team = None
    url = 'https://gzvr.tpondemand.com/api/v2/Teams?where=CustomValues["GitHubRepo"]=="' + repository['full_name'] + '"'
    logger.info('TargetProcess URL: ' + url)
    response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
    logger.info('TargetProcess Response: ' + response.text)
    data = response.json()
    teams = data['items']
    for teamTemp in teams:
        team = teamTemp

    # Valida se nao eh uma alteracao feita pelo GiHub e
    # se o projeto tem um repositorio configurado
    if (senderLogin != 'zavi-integrations') and (team is not None):
        if str(issue['labels']).find('userstory') > 0:
            urlComp = 'UserStories'
            urlComp2 = 'UserStory'
        elif str(issue['labels']).find('bug') > 0:
            urlComp = 'Bugs'
            urlComp2 = 'Bug'
        else:
            return 'Theres no valid "kind" label. Discarding issue.'

        # Verifica se a issue esta associada a uma entidade
        entity = None
        url = 'https://gzvr.tpondemand.com/api/v2/'+urlComp+'?select={id,project:{project.id,project.name,project.process}}&where=CustomValues["GitHubID"]=="' + str(issue['number']) + '" and team.id==' + str(team['id']) + ''
        logger.info('TargetProcess URL: ' + url)
        response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
        logger.info('TargetProcess Response: ' + response.text)
        data = response.json()
        entities = data['items']
        for entityTemp in entities:
            entity = entityTemp

        # O GitHub dispara dois hooks quando uma issue eh criada ja com um label e
        # duplica issues no TargetProcess. Para tratar isso, esse trecho garante
        # que so um dos hooks eh executado.
        if (entity is not None) or ((event['action']=='labeled') and (str(event['label']['name']).startswith('kind/'))):
    
            # Se a issue ja tiver uma entidade associada, retorna valores de processo e time
            if entity is not None:
                projectEnt = entity['project']
                process = projectEnt['process']['id']
            else:
                # Retorna o processo associado ao projeto
                url = 'https://gzvr.tpondemand.com/api/v1/Projects?format=json&where=Id%20eq%20' + str(262) #ID do placeholder do OKR
                response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
                logger.info('TargetProcess Response: ' + response.text)
                data = response.json()
                processes = data['Items']
                for processTemp in processes:
                    process = processTemp['Process']['Id']
                projectEnt = {'id': 262}
                    
            # Retorna os estados associados ao projeto
            url = 'https://gzvr.tpondemand.com/api/v1/EntityStates?format=json&where=(Process.Id eq ' + str(process) + ') and (EntityType.Name eq %27' + urlComp2 + '%27)'
            if issue['state'] == 'open' and len(issue['assignees']) == 0:
                url += ' and (IsPlanned eq %27true%27)'

            elif issue['state'] == 'open' and len(issue['assignees']) > 0:
                # Busca o estado Planned=true
                url2 = 'https://gzvr.tpondemand.com/api/v1/Entitystates?format=json&where=(Process.Id eq ' + str(process) + ') and (IsPlanned eq "True") and (EntityType.Name eq %27' + urlComp2 + '%27)'
                logger.info('TargetProcess URL: ' + url2)
                response2 = requests.get(url2, auth=(os.environ['user'], os.environ['pass']))
                logger.info('TargetProcess Response: ' + response2.text)
                data2 = response2.json()
                entityStates2 = data2['Items']
                for entityStateTemp2 in entityStates2:
                    numericPriority = entityStateTemp2['NumericPriority']

                url += ' and (NumericPriority gt ' + str(numericPriority) + ') and (IsFinal eq %27false%27)'

            elif issue['state'] == 'closed':
                url +=  ' and (IsFinal eq %27true%27)'

            logger.info('TargetProcess URL: ' + url)
            response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
            logger.info('TargetProcess Response: ' + response.text)
            data = response.json()
            entityStates = data['Items']
            for entityState in entityStates:
                stateId = entityState['Id']

            label = None
            labels = []

            for labelTemp in issue['labels']:
                labels.append(labelTemp)

            tags = []
            for label in labels:
                if not label['name'].startswith('kind/'):
                    tags.append(label['name'])

            if 'body' in issue and issue['body'] is not None: 
                body = '<!--markdown-->\n' + issue['body']
            else:
                body = ''

            # Atualiza a entidade no TargetProcess
            data = {'Name': issue['title'],
                    'Project': {'id' : projectEnt['id']},
                    'Team': {"id": team['id']},
                    'EntityState': {"id": stateId},
                    'Description': body,
                    'Tags': ','.join(map(str, tags)) , 
                    'CustomFields': [{'Name': 'GitHubID', 'Value': issue['number']}]
                  }
            
            if entity is not None:
                data['Id']= entity['id']
    
            url = 'https://gzvr.tpondemand.com/api/v1/'+urlComp+'?resultFormat=json'
            response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
            logger.info('TargetProcess Response: ' + response.text)
            
            if entity is None:
                # Comenta a URL do GH no TargetProcess
                responseEntity = response.json()
                data = {'Description': 'link : https://github.com/'+ repository['full_name'] + '/issues/' + str(issue['number']),
                        'General': {'ResourceType': "General", 'Id': responseEntity['Id']}}
                url = 'https://gzvr.tpondemand.com/api/v1/Comments?resultFormat=json'
                response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                
                # Comenta a URL do TP no GitHub
                data = {'body': 'link: https://gzvr.tpondemand.com/entity/' + str(responseEntity['Id'])}
                url = 'https://api.github.com/repos/' + repository['full_name'] + '/issues/' + str(issue['number']) + '/comments'
                response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))

            # Atualiza informacoes no GitHub
            data = {'labels' : labels}
            
            url = 'https://api.github.com/repos/' + repository['full_name'] + '/issues/' + str(issue['number'])
            response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
            gitHub = response.json()
            logger.info('GitHub Response: ' + response.text)

    return 'Hello World'
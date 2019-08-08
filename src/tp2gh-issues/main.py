import os
import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info('got event{}: ' + json.dumps(event))
    entity = event['Entity']
    
    # Retorna o nome do autor da alteracao
    author = event['Author']
    authorFirstName = author['FirstName']
    authorLastName = author['LastName']
    
    # Busca o repositorio no TargetProcess
    repo = None
    url = 'https://gzvr.tpondemand.com/api/v1/Teams/' + str(entity['SquadID']) + '?format=json'
    response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
    logger.info('TargetProcess Response: ' + response.text)
    data = response.json()
    customFields = data['CustomFields']
    for customField in customFields:
        if (customField['Name']=='GitHubRepo') and (customField.has_key('Value')):
            repo = customField['Value']
    
    # Valida se nao eh uma alteracao feita pelo GiHub e
    # se o projeto tem um repositorio configurado
    if (authorFirstName != 'Target') and (authorLastName != 'Process') and (repo is not None):

        # Se tiver uma issue do GitHub associada, retorna ela
        gitHubId = None
        customFields = entity['CustomFieldsMetaInfo']
        for customField in customFields:
            if (customField['Name']=='GitHubID') and (customField.has_key('Value')):
                gitHubId = customField['Value']
        
        # Retorna campos do json
        entityId = entity['ID']
        entityTitle = entity['Name']
        entityStateID = entity['EntityStateID']

        # Se nao tinha o numero da issue, atualiza no TP            
        if entity['EntityTypeName']=='Tp.BusinessObjects.UserStory':
            urlComp = 'UserStories'
        elif entity['EntityTypeName']=='Tp.BusinessObjects.Bug':
            urlComp = 'Bugs'

        # Busca o estado atual do card
        url = 'https://gzvr.tpondemand.com/api/v1/Entitystates?format=json&where=Id%20eq%20' + str(entityStateID)
        response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
        logger.info('TargetProcess Response: ' + response.text)
        data = response.json()
        entityStates = data['Items']
        for entityStateTemp in entityStates:
            entityState = entityStateTemp

        # Busca o estado Planned=true
        url = 'https://gzvr.tpondemand.com/api/v1/Entitystates?format=json&where=(Process.Id%20eq%20' + str(entityState['Process']['Id']) + ')%20and%20(IsPlanned%20eq%20"True")%20and%20(EntityType.Id%20eq%20' + str(entityState['EntityType']['Id']) + ')'
        response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
        logger.info('TargetProcess Response: ' + response.text)
        data = response.json()
        entityStates = data['Items']
        for entityStateTemp in entityStates:
            numericPriority = entityStateTemp['NumericPriority']
            plannedStateId = entityStateTemp['Id']
            
        #Busca as tags do card
        try:
            url = 'https://gzvr.tpondemand.com/api/v1/Generals/' + str(entityId) + '?format=json'
            response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
            logger.info('TargetProcess Response: ' + response.text)
            data = response.json()
            entityTags = data['Tags']
        except:
            logger.warning('Failed to return tags')
            entityTags = []


        #Busca o card relacionado (se existir)
        try:
            gitHubIdRelated = None
            if (entity.has_key('UserStoryID')) and (entity['UserStoryID'] != entity['ID']):
                url = 'https://gzvr.tpondemand.com/api/v1/Generals/' + str(entity['UserStoryID']) + '?format=json'
                response = requests.get(url, auth=(os.environ['user'], os.environ['pass']))
                logger.info('TargetProcess Response: ' + response.text)
                data = response.json()
                customFields = data['CustomFields']
                for customField in customFields:
                    if (customField['Name']=='GitHubID') and (customField.has_key('Value')):
                        gitHubIdRelated = customField['Value']
        except:
            logger.warning('Failed to return related id')
            entityTags = []

        if (gitHubId is not None) or (entityState['NumericPriority'] >= numericPriority):

            tags = []
            tags.append('kind/'+entity['EntityTypeName'].replace('Tp.BusinessObjects.', '').lower())
            if len(entityTags) > 0:
                tags.extend(entityTags.split(', '))

            data = {'labels': tags}

            if (event['OldEntity']['EntityStateID'] != entity['EntityStateID']):

                if (entityState['IsFinal'] is True) or (event['Modification'] == 'Deleted'):
                    data['state'] = 'closed'

                elif (entityState['IsFinal'] is False) and (entityState['IsPlanned'] is False):
                    data2 = {'Id': entityId, 'EntityState': {"id": plannedStateId}}

                    url = 'https://gzvr.tpondemand.com/api/v1/'+urlComp+'?resultFormat=json'
                    response = requests.post(url, json.dumps(data2), auth=(os.environ['user'], os.environ['pass']))
                    logger.info('TargetProcess Response: ' + response.text)

                    data['state'] = 'open'
                    data['assignee'] = None

                elif (entityState['IsPlanned'] is True):
                    data['state'] = 'open'
                    data['assignee'] = None            
            
            
            if gitHubId is not None:
                issue = '/' + gitHubId
            else:
                issue = ''
                data['title'] = entityTitle
            
            if str(event['ChangedFields']).find('Name') >= 0:
                data['title'] = entityTitle
            
            if entity.has_key('Description'):
                data['body'] = entity['Description']
            
            # Cria/atualiza a issue do GitHub
            url = 'https://api.github.com/repos/' + repo + '/issues' + issue
            logger.info('GitHub URL: ' + url)
            response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
            logger.info('GitHub Response: ' + response.text)
            gitHub = response.json()
            
            if gitHubId is None:
                # Comenta a URL do TP no GitHub
                gitHubId = gitHub['number']
                data = {'body': 'link: https://gzvr.tpondemand.com/entity/' + str(entityId)}
                url = 'https://api.github.com/repos/' + repo + '/issues/' + str(gitHubId) + '/comments'
                response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                logger.info('GitHub Response: ' + response.text)
                            
                # Comenta a issue relacionada, se houver
                if gitHubIdRelated is not None:
                    data = {'body': 'Related issue: #' + str(gitHubIdRelated)}
                    url = 'https://api.github.com/repos/' + repo + '/issues/' + str(gitHubId) + '/comments'
                    response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                    logger.info('GitHub Response: ' + response.text)

                data = {'Id': entityId, 'CustomFields': [{'Name': 'GitHubID', 'Value': gitHubId}]}
                url = 'https://gzvr.tpondemand.com/api/v1/'+urlComp+'?resultFormat=json'
                response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                logger.info('TargetProcess Response: ' + response.text)
                
                # Comenta a URL do GH no TargetProcess
                data = {'Description': 'link : https://github.com/'+ repo + '/issues/' + str(gitHubId),
                        'General': {'ResourceType': "General", 'Id': entityId}}
                url = 'https://gzvr.tpondemand.com/api/v1/Comments?resultFormat=json'
                response = requests.post(url, json.dumps(data), auth=(os.environ['user'], os.environ['pass']))
                logger.info('TargetProcess Response: ' + response.text)

    return 'Hello World'

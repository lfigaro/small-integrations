# GitHub - Add project label on issues

This integration intends to create project label identification on issues.

## Usage

On a project, just add a card to a project and wait for the integration to add a label 'project/xxxx-xxxx' where xxxx-xxxx is the name of the project.

### What if I don't want this to work on all the projects?

All projects whose name starts with # are ignored by this integration. :)

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user that will close the issue.
		- *pass*: password of this user.
	- Create a API Gateway to expose a URL to invoke your lambda function.
- Check 'Installation' section above adapting to your parameters to finish to install.
- Open your repo url
- On 'Settings' tab, click on 'Webhooks'
- Click on 'Add Webhook' and fullfill with the following parameters
	- Payload URL: The URL created before.
	- Content Type: application/json
	- Which events would you like to trigger this webhook?: Choose 'Let me select individual events.' and select 'Project cards' only.
	- Active: true
- Give colaboration permisson to the user created before.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
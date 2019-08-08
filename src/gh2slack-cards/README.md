# GitHub 2 Slack - Post a message when a card is added to a GitHub project

This integration intends to post a message in a slack specific channel when a card is added to a project.

## Usage

On a project, just add a card and wait for the integration to broadcast that on the configured slack channel.

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user.
		- *pass*: password of this user.
		- *sl_token*: token of slack application to use.
	- Create a API Gateway to expose a URL to invoke your lambda function.
- Check 'Installation' section above adapting to your parameters to finish to install.
- Open your repo url
- On 'Settings' tab, click on 'Webhooks'
- Click on 'Add Webhook' and fullfill with the following parameters
	- Payload URL: The URL created before.
	- Content Type: application/json
	- Which events would you like to trigger this webhook?: Choose 'Let me select individual events.' and select 'Project cards' only.
	- Active: true
- At the project description, add a line 'slack:xxxxxx' somewhere, where xxxxxx is the channel to broadcast the message
- Give repositories colaboration permission to the GitHub selected user.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
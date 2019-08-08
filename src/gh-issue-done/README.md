# GitHub - Issue Done

This integration intends to close a issue when one on a project move a card to a column named 'Done'

## Usage

On a project, just move a card to a column named 'Done' and see it being closed.

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user that will close the issue.
		- *pass*: password of this user.
	- Create a API Gateway to expose a URL to invoke your lambda function.
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
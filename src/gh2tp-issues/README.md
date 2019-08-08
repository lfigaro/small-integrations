# GitHub 2 TargetProcess - Export issues 

This integration intends to create a TargetProcess card every time a issue is created on GitHub


## Usage

- The issues labeled "kind/userstory" or "kind/bug" will automatically be replicated to TargetProcess.
- The title, body and comments are the pieces replicated.
- There are a few labels used by targetProcess to identify things:
	- Labels starting with "kind/" are used to identify the type of the card (story or bug).
	- Labels starting with "state/" are used to identify the state (column on TargetProcess).
	- Label "tp" identifies integrated issues.
Every other label are synchronized on TargetProcess tags.

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user that will close the issue.
		- *pass*: password of this user.
	- Create a API Gateway to expose a URL to invoke your lambda function.
- Check 'Installation' section above adapting to your parameters to finish to install.
- On TargetProcess
	- Add a custom text field called GitHubRepo at all projects on setup
	- Add the repository full path on the GitHubRepo field at the project configuration
	- Make sure to have 'planned' state configured in your process config
- On GitHub
	- Open your repo url
	- On 'Settings' tab, click on 'Webhooks'
	- Click on 'Add Webhook' and fullfill with the following parameters
		- Payload URL: The URL created before.
		- Content Type: application/json
		- Which events would you like to trigger this webhook?: Choose 'Let me select individual events.' and select 'Issues' only.
		- Active: true
	- Give repositories colaboration permission to the GitHub selected user.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
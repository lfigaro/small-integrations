# GitHub 2 Slack - Post message w/ current open discussions

This integration intends broadcast current GitHub discussions in Slack specific channels

## Usage

Every now and then (it depends on the CloudEvent recurrent schedule) a message will popup @ some channels. The integrations looks for channels named after the teams that the discussions are (a discussion on a team named 'engineering' will be showed on the channel 'engineering' at slack, if there's any).

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user that will close the issue.
		- *pass*: password of this user.
		- *sl_token*: token of slack application to use.
		- *org*: GitHub organization to look discussions on.
	- Create a Cloudevent schedule to start this function every now and then.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
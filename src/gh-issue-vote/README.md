# GitHub - Issue Voting

This integration is used to promote kind of a VOTING on GitHub projects. It counts :+1: reactions on the main comment on a issue and places a label "vote/XX", where XX is the number of reactions.

## Usage

At the body of an issue, add a :+1: reaction (A.K.A: thumbsup) and wait for at least a minute for the integration to add a label 'vote/XX' where XX is teh number of reactions. 

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user that will close the issue.
		- *pass*: password of this user.
		- *repos*: the GitHub repositories where the integration will work.
	- Schedule through CloudEvents for this lambda to run every minute.
- Give repositories colaboration permisson to the GitHub selected user.


## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
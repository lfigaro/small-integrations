# Workplace 2 Slack - Post broadcast

This integration intends to broadcast a message every time a post is created @ a Workplace specific group

## Usage

TODO

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *sl_token*: Slack API access token
		- *wp_token*: Workplace API access token
	- Create a API Gateway to expose a URL to invoke your lambda function.
- Check 'Installation' section above adapting to your parameters to finish to install.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
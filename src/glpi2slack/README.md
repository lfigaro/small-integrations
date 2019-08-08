# GLPI 2 Slack - broadcast issues summary

This integration intends to broadcast a message with a summary of open issues and the main categories for analisis

## Installation

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *app_token*: GLPI app token (configured in API client settings)
		- *authorization*: GLPI authorization header ('user_token <api-token>', configured in your personal profile settings)
		- *sl_channel*: lack channel to broadcast
		- *sl_token*: slack access token
		- *glpi_summary*: full api url (with parameters) that returns summary GLPI issues
		- *glpi_disturb*: full api url (with parameters) that returns users versus issues
		- *glpi_url*: GLPI api url 
	- Create a Cloudevent schedule to start this function every now and then.

## Usage

Every now and then (it depends on the CloudEvent recurrent schedule) a message will popup @ some channels.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.
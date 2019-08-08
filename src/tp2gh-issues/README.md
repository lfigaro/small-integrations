# TargetProcess 2 GitHub - Export issues 

This integration intends to create a GitHub issue every time a TargetProcess card is created

## Usage

- The Userstories or Bugs created at / updated to the planned state should appear as issues at the GitHub Repository (Note: You can check out which state is planned one at the "Process Setup").
- The title, body, comments and state changes will be replicated to GitHub
- Once the card reach the final state, the issue at GitHub will be closed.

## Wanna host this integration yourself?

Easy peasy. Just:

- Create a lambda function
	- Change 'Handler' to 'main.handler'
	- On 'Environment variables', create the following ones:
		- *user*: username of a GitHub integration user.
		- *pass*: password of this user.
	- Create a API Gateway to expose a URL to invoke your lambda function.
- Check 'Installation' section above adapting to your parameters to finish to install.
- On TargetProcess
	- Add a custom text field called GitHubRepo at all projects on setup
	- Add the repository full path on the GitHubRepo field at the project configuration
	- Make sure to have 'planned' state configured in your process config
	- Configure a webhook to call 
- On GitHub
	- Give repositories colaboration permission to the GitHub selected user.

## Credits

- Figaro (<https://github.com/lfigaro>)
- Lots more, run `git shortlog -s` for a list!

## License

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
BasecampHelper README
====

About
----

This is a small utility to help perform certain actions in [Basecamp](https://basecamp.com/).  
The main `basecamphelper.py` script can be run from the command line to perform the following actions:
- invite one or mulitple users to a project
- archive one or a group of projects
- post a message to multiple projects

The main function involves searching all projects in a given account for a string in the title, and performing the given action on every project that matched the search.

The `autopost.py` can be set as a `cron` job to automatically run. In my install, this is set to run in `crontab` once per minute. It relies on the [`PyEmailWatcher`](https://github.com/jasongtz/PyEmailWatcher) submodule to monitor an inbox.
This allows users to send an email to a given address, specifying a search query, and have the message posted to every project that matches the search.

-----

### Using `autopost` Email (Syntax)

The email must be formatted exactly as below for the emails to be picked up by `PyEmailWatcher`.

Email Subject: 
> POST, {search string}, {New Post Title}

Body: 
> plain text message content



Upcoming
------

~~- Batch add a group of users to a project (built, in testing)~~ - resolved
- When PyEmailWatcher is on PyPI, change from submodule to setup.py or requirements.txt

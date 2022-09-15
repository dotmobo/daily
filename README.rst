
Daily Scrum Report Bot
======================
Generate a daily scrum report from gitlab and post it on a mattermost channel.

Install and use
---------------

* Install python 3.9 and poetry (https://python-poetry.org/)
* Configure **config.ini**
* `poetry install`
* `poetry run daily` : local message only
* `poetry run daily 1 true` : message sent to mattermost

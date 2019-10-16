# slack-list-members
List members of a Slack channel by alias, email, name, and title

```
% python3 slack-list-members.py osx
[...]
dwing        danwing@github.com               Dan Wing                       security, networking, ☕ ð⛷️   
```

```
% python3 slack-list-members.py -h     
usage: slack-list-members.py [-h] [-d] [-t TOKEN_FILE] [-V] channel_name

List members of a Slack channel by alias, name, and email address

positional arguments:
  channel_name   Slack channel name

optional arguments:
  -h, --help     show this help message and exit
  -d             debug output
  -t TOKEN_FILE  file containing Slack legacy token, if not using
                 SLACK_API_TOKEN environment variable
  -V             show program's version number and exit
```
#!/usr/bin/env python

#
# slack-list-members.py
# List members of a Slack channel by alias, email, name, and title
# September 2019, Dan Wing
#

import sys
if sys.version_info.major < 3:
    sys.exit ("need Python 3, running " + str(sys.version_info.major) + 
              "." + str(sys.version_info.minor))

import os, slack, argparse, urllib.parse, logging
MAX_PAGINATION = 999

#-----
#
# process CLI arguments
ap = argparse.ArgumentParser(
    description=
    'List members of a Slack channel by alias, name, and email address')
ap.add_argument('-d',
                dest='debug',
                required=False,
                default=False,
                help='debug output',
                action='store_true')
ap.add_argument(
    '-t',
    dest='token_file',
    required=False,
    type=argparse.FileType('r'),
    help=
    'file containing Slack legacy token, if not using SLACK_API_TOKEN environment variable'
)
ap.add_argument('channel_name', nargs=1, help='Slack channel name')
ap.add_argument('-V', action='version', version='%(prog)s 1.0')
args = vars(ap.parse_args())

CHANNEL_NAME = args['channel_name'][0]
if args['debug']: logging.basicConfig(level=getattr(logging, "DEBUG", None))

# get API token from environment variable and allow -t to override
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
if args['token_file']: SLACK_API_TOKEN = args['token_file'].read().rstrip()

if not SLACK_API_TOKEN:
    sys.exit(
        'missing Slack API token. Supply via SLACK_API_TOKEN environment variable or -t.\n\
generate API token at https://api.slack.com/custom-integrations/legacy-tokens')


#------
#
# fetch all channels this API token belongs to
client = slack.WebClient(SLACK_API_TOKEN)

conversations = client.users_conversations(
    types='private_channel,public_channel')

for pagination in range(MAX_PAGINATION):
    #-----
    #
    # translate human-readable channel name into Slack's channel-id
    channel_id = None
    for c in conversations['channels']:
        logging.debug(c['name'])
        if c['name'] == CHANNEL_NAME:
            channel_id = c['id']
            break

    if not channel_id and conversations['response_metadata']['next_cursor']:
        conversations = client.users_conversations(
            types='private_channel,public_channel',
            limit=3,
            cursor=conversations['response_metadata']['next_cursor'])
    else:
        break

if not channel_id:
    sys.exit('channel \"' + CHANNEL_NAME +
             '\" not among this Slack API Token\'s list of channels')

logging.debug('Channel ' + CHANNEL_NAME + ' has id ' + channel_id)


#------
#
# get members of that Channel ID
channel_info = client.conversations_members(channel=channel_id)
logging.debug(channel_info)

for pagination in range(MAX_PAGINATION):

    members = channel_info['members']
    logging.debug(members)

    #------
    #
    # retrieve details for each member
    for member in members:
        user_info = client.users_info(user=member)
        logging.debug(user_info)
        if user_info['user']['deleted'] or user_info['user']['is_bot']: continue

        print('{!s:12} {!s:<35} {!s:<30} {!s:<30}'.format(
            user_info.get('user', {}).get('profile', {}).get('display_name'),
            user_info.get('user', {}).get('profile', {}).get('email'),
            user_info.get('user', {}).get('profile',
                                          {}).get('real_name_normalized'),
            user_info.get('user', {}).get('profile', {}).get('title')))

    if channel_info['response_metadata']['next_cursor']:
        channel_info = client.conversations_members(
            channel=channel_id,
            cursor=channel_info['response_metadata']['next_cursor'])
    else:
        break

sys.exit()

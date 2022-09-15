
from datetime import datetime
from pandas.tseries.offsets import BDay
import sys
import configparser
from .bcolors import bcolors
from .gitlab import get_response_from_gitlab
from .mattermost import send_message

##############################################
#  Daily Scrum                               #
#  python3 main.py <days> <enable_mattermost #
##############################################


def run():
    config = configparser.ConfigParser()
    config.read("config.ini")
    url = config["gitlab"]["url"]
    token = config["gitlab"]["token"]
    user = config["gitlab"]["user"]
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    since = datetime.now() - BDay(days)
    enable_mattermost = bool(sys.argv[2]) if len(sys.argv) > 2 else False

    matt_url = config["mattermost"]["url"]
    matt_pass = config["mattermost"]["password"]
    matt_user = config["mattermost"]["user"]
    matt_channel = config["mattermost"]["channel"]

    message = f"\n{bcolors.OKGREEN}Daily du {datetime.strftime(datetime.now(), '%d/%m/%Y')}{bcolors.ENDC}\n"
    message_matt = f"\n#daily **Daily du {datetime.strftime(datetime.now(), '%d/%m/%Y')}**\n"

    response = get_response_from_gitlab(url, token, user, since)

    message += f"\nDepuis le {datetime.strftime(since, '%d/%m/%Y')},"
    message_matt += f"\nDepuis le *{datetime.strftime(since, '%d/%m/%Y')}*,"

    for project_name, commits in response.items():
        if len(commits) > 0:
            message += f"\nSur le projet {bcolors.WARNING}{project_name}{bcolors.ENDC}, j'ai développé les fonctionnalités suivantes:\n"
            message_matt += f"\nSur le projet **{project_name}**, j'ai développé les fonctionnalités suivantes:\n"
            for commit in commits:
                message += f"\t{bcolors.OKBLUE}{commit.message.strip()}{bcolors.ENDC} ({commit.web_url})\n"
                message_matt += f"\t{commit.message.strip()} *({commit.web_url})*\n"

    print(message)
    if(enable_mattermost):
        print("Send message to mattermost...")
        send_message(matt_url, matt_user, matt_pass, matt_channel, message_matt)


if __name__ == "__main__":
    run()

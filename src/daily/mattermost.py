from mattermost import MMApi

def send_message(url, user, password, channel, message):
  mm = MMApi(url)
  mm.login(user, password)
  mm.create_post(channel, message)
  mm.revoke_user_session()
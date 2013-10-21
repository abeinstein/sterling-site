import sleekxmpp
import logging

from .models import Suggestion

logging.basicConfig(level=logging.DEBUG)

server = ('chat.facebook.com', 5222)

class SendMsgsBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, recipients, message, suggestion_list):
        sleekxmpp.ClientXMPP.__init__(self, jid, 'ignore')
        self.recipients = recipients
        self.message = message
        self.suggestion_list = suggestion_list
        self.add_event_handler("session_start", self.start, threaded=False)
    
    def start(self, event):
        self.send_presence()
        self.get_roster()
        for recipient_id in self.recipients:
            recipient = '-' + recipient_id + '@chat.facebook.com'

            sug = Suggestion.objects.get(app_user__facebook_id=recipient_id, suggestion_list=self.suggestion_list)
            self.message += " %s" % sug.link

            self.send_message(mto=recipient, mbody=self.message, mtype='chat')
        
        self.disconnect(wait=True)


def send_invitations_via_facebook_message(suggestion_list, friends_invited):
    mobile_app = suggestion_list.app_user_membership.mobile_app
    app_user = suggestion_list.app_user_membership.app_user
    invitation_message = mobile_app.invitation_message
    oauth_token = suggestion_list.app_user_membership.oauth_token

    sender = app_user.facebook_id + '@chat.facebook.com'
    xmpp = SendMsgsBot(sender, friends_invited, invitation_message, suggestion_list)
    xmpp.credentials['api_key'] = mobile_app.facebook_id
    xmpp.credentials['access_token'] = oauth_token
        
    if xmpp.connect(server):
        xmpp.process(block=True)
        return True
    else:
        print "Error"
        return False
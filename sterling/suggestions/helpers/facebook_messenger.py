import sleekxmpp

logging.basicConfig(level=logging.DEBUG)

server = ('chat.facebook.com', 5222)

class SendMsgsBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, recipients, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, 'ignore')
        self.recipients = recipients
        self.message = message
        self.add_event_handler("session_start", self.start, threaded=False)
    
    def start(self, event):
        self.send_presence()
        self.get_roster()
        for recipient_id in self.recipients:
            recipient = '-' + recipient_id + '@chat.facebook.com'
            self.send_message(mto=recipient, mbody=self.message, mtype='chat')
        
        self.disconnect(wait=True)

def send_invitations_via_facebook_message(sender, friends_invited, invitation_message, oauth_token, app_facebook_id):
    sender = sender + '@chat.facebook.com'
    xmpp = SendMsgsBot(sender, friends_invited, invitation_message)
    xmpp.credentials['api_key'] = app_facebook_id
    xmpp.credentials['access_token'] = oauth_token
        
    if xmpp.connect(server):
        import pdb; pdb.set_trace()

        xmpp.process(block=True)
        return True
    else:
        print "Error"
        return False
import sleekxmpp

server = ('chat.facebook.com', 5222)

from_id = '1141801163@chat.facebook.com'
to_id = '-1247010773@chat.facebook.com'
message = 'Curiously sent via a python/XMPP solution'

class SendMsgsBot(sleekxmpp.ClientXMPP):
	def __init__(self, jid, recipients, message):
		sleekxmpp.ClientXMPP.__init__(self, jid, 'ignore')
		self.recipients = recipients
		self.message = message
		self.add_event_handler("session_start", self.start, threaded=True)
	
	def start(self, event):
		self.send_presence()
		self.get_roster()
		for recipient in self.recipients:
			self.send_message(mto=recipient, mbody=self.message, mtype='chat')
		
		self.disconnect(wait=True)


def send_invitations_by_fb_message(inviter_id, invited_list, message, o_auth_token):
	xmpp = SendMsgsBot(inviter_id, invited_list, message)
	xmpp.credentials['api_key'] = '466489223450195'
	xmpp.credentials['access_token'] = o_auth_token
		
	if xmpp.connect(server):
		xmpp.process(block=True)

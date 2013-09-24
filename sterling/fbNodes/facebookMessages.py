import sleekxmpp
import logging

logging.basicConfig(level=logging.DEBUG)

server = ('chat.facebook.com', 5222)

class SendMsgsBot(sleekxmpp.ClientXMPP):
	def __init__(self, jid, recipients, message):
		sleekxmpp.ClientXMPP.__init__(self, jid, 'ignore')
		self.recipients = recipients
		self.message = message
		self.add_event_handler("session_start", self.start, threaded=False)
	
	def start(self, event):
		print "4"
		self.send_presence()
		self.get_roster()
		print "5"
		for recipient_id in self.recipients:
			recipient = '-' + str(recipient_id) + '@chat.facebook.com'
			self.send_message(mto=recipient, mbody=self.message, mtype='chat')
		
		self.disconnect()
	


def send_facebook_messages(inviter_id, invited_list, message, o_auth_token):
	inviter = str(inviter_id) + '@chat.facebook.com'
	xmpp = SendMsgsBot(inviter, invited_list, message)
	xmpp.credentials['api_key'] = '422143484562527'
	xmpp.credentials['access_token'] = o_auth_token
		
	if xmpp.connect(server):
		print "3"
		xmpp.process(block=True)
		#xmpp.start({})
		print "6"
	else:
		print "Error"

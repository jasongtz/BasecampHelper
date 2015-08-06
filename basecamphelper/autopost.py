# auto.py

from PyEmailWatcher.pyemailwatcher.pyemailwatcher import Watcher
import basecamphelper as b
import json, os

def main():

	with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r')  as fp:
		config = json.loads(fp.read())

	b.url =  "https://basecamp.com/%s" % config['account_id']
	
	b.headers = {}
	b.headers['content-type'] = 'application/json'
	b.headers['user-agent'] = config['user-agent']

	b.creds = [config['username'], config['password']]
		
	login = Watcher(config['username'], config['password'],
		config['imap_server'], config['smtp_server'], smtp_port=587, confirm_from='BasecampHelper', smtp_tls=True)
	
	login.connect()
	results = login.search('POST, ')
	
	for e in results:
		uid, email = e
		# Email subject: POST, Projects_search_string, MessageTitle
		header, query, title = email['subject'].split(", ")
	
		if email.get_content_maintype() == 'text':
			body = email.get_payload(decode=True) # added decode=True
			body = decode_email(body)

		elif email.get_content_maintype() == 'multipart':
			for part in email.walk():
				if part.get_content_maintype() == 'text':
					body = part.get_payload(decode=True)
					body = decode_email(body)
					break
		
		projects = b.get_all_groups(query)
		for project_id in projects:
			b.post_message(project_id, title, body)
		
		login.confirm(uid, email)
	login.logout()

def decode_email(text):
	if '<html>' in text.splitlines()[0]:
		return text
	try:
		body = unicode(text, 'utf8')
	except UnicodeDecodeError:
		body = unicode(text, 'Cp1252')
	return body
	### Consider using part.get_content_charset() and decoding that

if __name__ == "__main__":
	main()
# autowatchduedate

import basecamphelper as b
from PyEmailWatcher.pyemailwatcher.pyemailwatcher import Watcher
import json, requests, datetime, re

def get_todo_list():
	
	todolist = requests.get(url + "/api/v1/todolists.json",
		auth=(creds[0], creds[1]), headers=headers)

	todolist = todolist.json()

	for lists in todolist:
		if config['todolist_name'] in lists['name'].lower():
			# todolist_name should be in the config file
			# that will be the search query for the todo list to watch
			return lists['id'], lists['bucket']['id']

def get_todos(todolist, project_id):
	todos = requests.get(url + "/api/v1/projects/%s/todolists/%s/todos.json" 
		% (project_id, todolist), auth=(creds[0], creds[1]), headers=headers)
	todos = todos.json()
	
	items_due = [] # list of dicts
	for item in todos:
		try:
			todo_details = {
				'name':item['content'], # tuple (content, due_on)
				'due_on':datetime.datetime.strptime(item['due_on'], "%Y-%m-%d"),
				'last_comment':get_last_comment(project_id, item['id'])
			}
			# check if the item is due yet
			if todo_details['due_on'] <= datetime.datetime.today():
				items_due.append(todo_details)

		except TypeError as e:
			# Skips todos that don't have a duedate, ie j['due_on'] = None
			if 'None' in str(e): 
				continue
	return items_due

def get_last_comment(project_id, todo_id):
	todo_object = requests.get(url + "/api/v1/projects/%s/todos/%s.json"
		% (project_id, todo_id), auth=(creds[0], creds[1]), headers=headers)
	last_comment = todo_object.json()['comments'][-1] # list of comment objects
	return last_comment['content']

def email_loaner(item):
	login = Watcher(config['username'], config['password'],
		config['imap_server'], config['smtp_server'], 
		smtp_port=587, confirm_from='Your Equipment On Loan', smtp_tls=True)
	login.connect()
	due = item['due_on'].strftime('%d-%m-%Y')

	with open(os.path.join(os.path.dirname(__file__), 'message.txt'), 'r') as fp:
		message = fp.read()
	message = message.replace('{{ item }}', item['name']).replace('{{ due_date }}', due)
	print item['last_comment']
	try:
		login.send_confirmation(message, [creds[0], item['last_comment']])
	except:
		try:
			login.send_confirmation('ERROR: UNABLE TO SEND:\n\n\n' + message, [creds[0]])
		except:
			raise

def main():
	global url
	global headers
	global creds
	global config
	with open('basecamphelper/config.json', 'r')  as fp:
		config = json.loads(fp.read())

	url =  "https://basecamp.com/%s" % config['account_id']
	
	headers = {}
	headers['content-type'] = 'application/json'
	headers['user-agent'] = config['user-agent']

	creds = [config['username'], config['password']]

	list_id, project_id = get_todo_list()
	due_list = get_todos(list_id, project_id)
	for item in due_list:
		email_loaner(item)

if __name__ == "__main__":
	main()
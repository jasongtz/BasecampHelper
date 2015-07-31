# autowatchduedate

import basecamphelper as b
from PyEmailWatcher.pyemailwatcher.pyemailwatcher import Watcher
import json, requests, datetime

def get_todo_list():
	
	todolist = requests.get(url + "/api/v1/todolists.json",
		auth=(creds[0], creds[1]), headers=headers)

	todolist = todolist.json()

	for i in todolist:
		if 'on loan' in i['name'].lower():
			# 'on loan' is the search query we're watching for
			return i['id'], i['bucket']['id']

def get_todos(todolist, project_id):
	todos = requests.get(url + "/api/v1/projects/%s/todolists/%s/todos.json" 
		% (project_id, todolist), auth=(creds[0], creds[1]), headers=headers)
	todos = todos.json()
	
	items_due = [] # list of tuples
	for j in todos:
		items_due.append((j['content'],
			 datetime.datetime.strptime(j['due_on'], "%Y-%m-%d")))
	return items_due

def main():
	with open('basecamphelper/config.json', 'r')  as fp:
		config = json.loads(fp.read())
	global url
	global headers
	global creds
	url =  "https://basecamp.com/%s" % config['account_id']
	
	headers = {}
	headers['content-type'] = 'application/json'
	headers['user-agent'] = config['user-agent']

	creds = [config['username'], config['password']]

	list_id, project_id = get_todo_list()
	due_list = get_todos(list_id, project_id)
	print due_list

if __name__ == "__main__":
	main()
# Create Basecamp users

import requests, json, csv, os, sys
	
def get_all_groups(query):
	params = {}
	
	try:
		response = requests.get(url + "/api/v1/projects.json", \
			auth=(creds[0], creds[1]), headers=headers)
	except:
		print "REQUESTS ERROR!"
		try:
			print response.json()
		except:
			print "Unable to print error report."

	all_group_ids = []
	for i in response.json():
		if query.lower() in i['name'].lower():
			print "Retrieved group: " + i['name']
			all_group_ids.append(i['id'])

	if len(all_group_ids) == 0:
		print 'No groups matched.\n'
		get_all_groups()
	return all_group_ids
		

def add_to_project(projectid, emaillist):
	params = {}

	for email in emaillist:

		accesses = requests.get(url + "/api/v1/projects/%s/accesses.json" \
			% projectid, auth = (creds[0], creds[1]), headers = headers)
		list_of_accesses = [i['email_address'] for i in accesses.json()]

		if email not in list_of_accesses:

			params["email_addresses"] = email

			response = requests.post(url + "/api/v1/projects/%s/accesses.json" \
				% projectid, auth=(creds[0], creds[1]), data=json.dumps(params), headers=headers)
			print response

			if "204" in str(response):
				print "Added " + str(params['email_addresses']) + " to project.\n"
			else:
				print "An error occured." + str(response)
				with open("error_log.txt", "a") as fp:
					fp.write("\n\nError processing: %s" % params["email_addresses"])
					fp.write("\Group: %s" % projectid)
				try:
					print response.json()
				except:
					pass

def archive_project(projectid):

	params = {'archived':True}
	
	response = requests.put(url + "/api/v1/projects/%s.json" % projectid, \
		auth=(creds[0], creds[1]), data=json.dumps(params), headers=headers)

	if "200" in str(response):
		print "Archived project: %s" % projectid
	else:
		print "An error occured." + str(response)
		with open("error_log.txt", "a") as fp:
			fp.write("\n\nError processing: %s" % projectid)
		try:
			print response.json()
		except:
			pass

def post_message(projectid, title, body):
	
	message = {}
	message['subject'] = title
	message['content'] = body
	
	response = requests.post(url + "/api/v1/projects/%s/messages.json" % projectid, \
		auth=(creds[0], creds[1]), data=json.dumps(message), headers=headers)

	if "201" in str(response):
		print "Posted message to: %s" % projectid
	else:
		print "An error occured." + str(response)
		with open("error_log.txt", "a") as fp:
			fp.write("\n\nError processing: %s" % projectid)
		try:
			print response.json()
		except:
			pass


def main():

	print "Retrieving all projects..."
	print "Please enter your search query:"
	projectids = get_all_groups(raw_input(">>> "))

	
	print "\n\n"
	for index, app in enumerate(applist):
		print "%s. %s" % (index, app)
	
	appchoice = int(raw_input("Which function to launch: "))

	if appchoice == 0:
		list_to_add = raw_input("Comma-seperated list of email addresses: ").split(", ")		
		for id in projectids:
			add_to_project(id, list_to_add)

	elif appchoice == 1:
		for id in projectids:
			archive_project(id)

	elif appchoice == 2:
		title = raw_input("Title: ")
		body = raw_input("Body: ")
		for id in projectids:
			post_message(id, title, body)


if __name__ == "__main__":

	with open('config.json', 'r')  as fp:
		config = json.loads(fp.read())

	applist = [
		'Add users to projects',
		'Archive projects',
		'Post message to projects',
		]

	url =  "https://basecamp.com/%s" % config['account_id']
	
	headers = {}
	headers['content-type'] = 'application/json'
	headers['user-agent'] = config['user-agent']

	creds = [config['username'], config['password']]

	main()

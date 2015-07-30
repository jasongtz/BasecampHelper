# Create Basecamp users

import requests, json, csv, os
import basecamphelper

def readfile():

	while True:
		print "Please drag in the CSV file:"
		filename = raw_input(">>> ").replace("\\", "")[:-1] # Strips the slash and trailing space
		if os.path.exists(filename):
			break
		else:
			print "Error loading file. Try again."

	with open(filename, "r") as fp:
		read = [line for line in csv.reader(fp)]
	studentlist = []

	for x in range(1, len(read)):
		parsed = {}
		#read[0][y] = HEADER
		#read[x][y] = CELL
		for y in range(len(read[0])):

			if read[x][y] and read[x][y] != ' ':		
				parsed[read[0][y]] = read[x][y]

		if len(parsed.keys()) > 0:
			studentlist.append(parsed)

	groupdict = {}

	for student in studentlist:
		if student[groupname] not in groupdict:
			groupdict[student[groupname]] = [student]
		else:
			groupdict[student[groupname]].append(student)
	return groupdict
	
def create_group(name):

	params = {}
	params["name"] = name

	response = requests.post(url + "/api/v1/projects.json", \
		auth=(creds[0], creds[1]), data=json.dumps(params), headers=headers)

	try:
		response = response.json()
		print "Created Project: " + response["name"] + ", ID: " + str(response['id'])
		return response['id']
	except:
		print "REQUESTS ERROR!"
		try:
			print response.json()
		except:
			print "Unable to print error report."
		

def add_students(projectid, students):
	params = {}

	params["email_addresses"] = [i[email] for i in students]

	response = requests.post(url + "/api/v1/projects/%s/accesses.json" \
		% projectid, auth=(creds[0], creds[1]), data=json.dumps(params), headers=headers)

	print response
	print response.text

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


def main():

	print "Starting Basecamp project creation and invites..."

	filedata = readfile()
	for item in filedata.items():
		projectid = create_group(item[0])
		add_students(projectid, filedata[item[0]])

if __name__ == "__main__":

	with open('config.json', 'r')  as fp:
		config = json.loads(fp.read())

	url =  "https://basecamp.com/%s" % config['account_id']
	
	headers = {}
	headers['content-type'] = 'application/json'
	headers['user-agent'] = config['user-agent']

	creds = [config['username'], config['password']]

	print "Please type the header representing the group name:"
	groupname = raw_input(">>> ")
	print "Please type the header representing the email:"
	email = raw_input(">>> ")

	main()


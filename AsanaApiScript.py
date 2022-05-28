import asana
import json

# https://github.com/Asana/python-asana



##########   AUTHENTICATION AND INITIAL SETUP ###########

def getSettings():
	# The following file should contain the following json properties:
	#   - personalAccessToken
	fileName = "AsanaSettings.json"
	with open(fileName) as file:
		return json.load(file)

settings = getSettings()

def getClient():
	client = asana.Client.access_token(settings['personalAccessToken'])
	client.options['client_name'] = "Asana Python Script"
	return client

client = getClient()

me = client.users.me()
orgId = me['workspaces'][0]['gid']
userId = me['gid']
print("Authenticated for Asana with email " + me['email'] + ", name " + me['name'] + ", and ID " + userId + ".")



##########   DRAFT STUFF NOT USED   ###########

#orgTeams = list(client.teams.get_teams_for_organization(orgId))
#print("Teams: " + str(len(orgTeams)))

#myTeams = list(client.teams.get_teams_for_user("me", {"organization": orgId}))
#for team in myTeams:
#	print(team)
#	projects = list(client.projects.get_projects_for_team(team['gid']))
#	for project in projects:
#		print(project)
#print("My Teams: " + str(len(myTeams)))



##########   THE ACTUAL LOGIC   ###########

def writeUsersToFile():
	users = client.users.get_users_for_workspace(orgId, {"opt_fields": ["email"]})
	userString = ""
	for user in users:
		userString += user['email'] + "\n"
	with open("Output-AsanaUsers.txt", "w") as file:
		file.write(userString)
	print("Wrote users to file.")

def createTask():
	# https://asana.readthedocs.io/en/latest/
	print("Creating a task:")
	title = input("    Enter title of task: ")
	description = input("    Enter description of task: ")
	task = client.tasks.create_task({'workspace': orgId, 'name': title, 'assignee': userId, 'notes': description})


##########   CALLING THE ACTUAL LOGIC   ###########

writeUsersToFile()
createTask()

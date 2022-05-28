import asana
import json
import os
from datetime import datetime

# https://github.com/Asana/python-asana



##########   AUTHENTICATION AND INITIAL SETUP ###########

def clear(): os.system('clear')

clear()
print("Initializing and authenticating...")

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



##########   THE ACTUAL LOGIC   ###########

def writeToFile(content, fileName):
	with open("Output-" + fileName, "w") as file:
		file.write(content)

def writeTeamsToFile():
	teams = client.teams.get_teams_for_organization(orgId)
	output = "\n".join(map(str, teams))
	writeToFile(output, "Teams.txt")
	print("Wrote teams to file.")

def writeMyTeamsAndProjectsToFile():
	myTeams = list(client.teams.get_teams_for_user("me", {"organization": orgId}))
	output = ""
	for team in myTeams:
		teamId = team['gid']
		output += "Team: \n" + team['name'] + " (" + teamId + ")\n\n Projects: \n"
		projects = client.projects.get_projects_for_team(teamId)
		output += "\n".join(map(lambda project: "  - " + project['name'] + " (" + project['gid'] + ")", projects)) + "\n\n\n\n"
	writeToFile(output, "MyTeamsAndProjects.txt")
	print("Wrote my teams and projects to file.")

def writeUsersToFile():
	users = client.users.get_users_for_workspace(orgId, {"opt_fields": ["email"]})
	usersString = "\n".join(map(lambda user: user['email'], users))
	writeToFile(usersString, "AsanaUsers.txt")
	print("Wrote users to file.")

def createTask():
	# https://asana.readthedocs.io/en/latest/
	print("Creating a task:")
	title = input("    Enter title of task: ")
	if title == "": return
	description = input("    Enter description of task: ")
	task = client.tasks.create_task({'workspace': orgId, 'name': title, 'assignee': userId, 'notes': description})

def writeMyTasks():
	now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	tasks = client.tasks.find_all({"opt_fields": ["projects", "name", "due_on"]}, completed_since = now, workspace = orgId, assignee = userId)
	output = "\n".join(map(str, tasks))
	writeToFile(output, "MyTasks.txt")
	print("Wrote my tasks to file.")



##########   CALLING THE ACTUAL LOGIC   ###########

while 0 == 0:
	print('1: Create task')
	print('2: Output users, teams, my teams & projects, and my tasks')
	task = input("Enter your choice: ")
	match task:
		case '1':
			createTask()
		case '2':
			writeUsersToFile()
			writeTeamsToFile()
			writeMyTeamsAndProjectsToFile()
			writeMyTasks()
		case _:
			break
	clear()

import asana
import json
import os
from datetime import datetime

# https://github.com/Asana/python-asana
# https://asana.readthedocs.io/en/latest/
# https://juaancabsou.medium.com/asana-automation-with-python-63c32c46c666
# https://stackoverflow.com/questions/30601424/how-can-i-create-a-new-project-with-tasks-in-asana-using-python



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
	print("Creating a task:")
	title = input("    Enter title of task: ")
	if title == "": return
	description = input("    Enter description of task: ")
	task = client.tasks.create_task({'workspace': orgId, 'name': title, 'assignee': userId, 'notes': description})

def writeMyIncompleteTasks():
	now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	tasks = client.tasks.find_all({"opt_fields": ["projects", "name", "due_on"]}, completed_since = now, workspace = orgId, assignee = userId)
	output = "\n".join(map(str, tasks))
	writeToFile(output, "MyIncompleteTasks.txt")
	print("Wrote my incomplete tasks to file.")

def writeAllMyTasks():
	tasks = client.tasks.find_all({"opt_fields": ["projects", "name", "due_on", "completed", "created_at", "modified_at", "completed_at"]}, workspace = orgId, assignee = userId)
	output = "\n".join(map(str, tasks))
	writeToFile(output, "AllMyTasks.txt")
	print("Wrote all my tasks to file.")

def investigateMyTasks():
	myTasks = client.user_task_lists.get_user_task_list_for_user(userId, workspace = orgId)
	print(myTasks)
	myTasksId = myTasks['gid']
	sections = client.sections.get_sections_for_project(myTasksId)
	output = "\n".join(map(str, sections))
	print(output)



##########   CALLING THE ACTUAL LOGIC   ###########

while 0 == 0:
	print("\n\nSelect what you'd like to do:")
	print('1: Create task')
	print("2: Output my tasks")
	print("3: Output all users, all teams, my teams, and my projects")
	print("4: Investigate 'My tasks'")
	task = input("Enter your choice: ")
	match task:
		case '1':
			createTask()
		case '2':
			writeMyIncompleteTasks()
			writeAllMyTasks()
		case '3':
			writeUsersToFile()
			writeTeamsToFile()
			writeMyTeamsAndProjectsToFile()
		case "4":
			investigateMyTasks()
		case _:
			break

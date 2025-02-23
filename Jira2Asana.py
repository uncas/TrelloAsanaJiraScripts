# Built on Python 3

# This script can assist in migrating a list of Jira tasks to Asana.

import csv
import glob
from datetime import datetime
from collections import Counter

# Set this to a positive number if you want to include only a few rows for testing:
# TODO: Set this to 0 when running with complete data:
sampleSize = 0

def convertJiraCsvToAsanaCsv(jiraCsvFileName):
	fileNameWithoutExtension = jiraCsvFileName[:-4]

	logFileName = "Log-" + fileNameWithoutExtension + ".txt"
	logFile = open(logFileName, 'w')
	def log(message):
		logFile.writelines([message + "\n"])

	def getValues(row, fieldName):
		return [value for index, value in enumerate(row) if value and header[index] == fieldName]

	def getValue(row, fieldName):
		values = getValues(row, fieldName)
		return "\n".join(values)

	def getComments(row):
		comments = getValues(row, "Comment")
		comments = ["Comment: " + value for value in comments]
		return "\n\n".join(comments)

	def getCollaborators(row, people):
		watchers = [x for index, x in enumerate(row) if x and header[index] == "Watchers"]
		collaborators = set([x for x in people + watchers if "@schibsted.com" in x])
		return ",".join(collaborators)

	asanaCsvFileName = "Asana-" + fileNameWithoutExtension + ".csv"
	asanaCsvfile = open(asanaCsvFileName, 'w')
	csvwriter = csv.writer(asanaCsvfile, dialect='excel')
	csvwriter.writerow(['Name', 'Description', 'Assignee', 'Collaborators', 'Due Date', 'Section / Column', 'Subtask of', 'Status', 'Priority', 'Type', 'Created by', 'Components', 'Labels', 'JiraKey', 'Created on', 'Platform'])

	def mapAndWriteRow(row):
		title = getValue(row, "Summary")
		status = getValue(row, "Status")
		priority = getValue(row, "Priority")
		issueType = getValue(row, "Issue Type")
		sprint = getValue(row, "Sprint")
		dueDate = None
		subtaskOf = None
		assignee = getValue(row, "Assignee")
		jiraKey = getValue(row, "Issue key")
		components = ",".join(getValues(row, "Component/s"))
		created = getValue(row, "Created")
		year = "CreatedIn-" + created[6:10]
		labels = getValues(row, "Labels")
		labels.append(year)
		labelsField = ",".join(labels)
		project = getValue(row, "Project name")

		createdDate = datetime.strptime(created[:10], '%d.%m.%Y')
		createdField = datetime.strftime(createdDate, '%m/%d/%y')

		jiraLink = "https://jira.schibsted.io/browse/" + jiraKey
		reporter = getValue(row, "Reporter")
		creator = getValue(row, "Creator")
		updated = getValue(row, "Updated")
		description = getValue(row, "Description")
		comments = getComments(row)
		collaborators = getCollaborators(row, [reporter, creator])

		descriptionField = "Jira Link: " + jiraLink
		descriptionField += "\nReporter: " + reporter
		descriptionField += "\nCreator: " + creator
		descriptionField += "\nLast updated: " + updated
		if description: descriptionField += "\n\n" + description
		if comments: descriptionField += "\n\n" + comments

		createdByField = reporter if "@schibsted.com" in reporter else None
		assigneeField = assignee if "@schibsted.com" in assignee else None
		section = sprint if sprint else "Backlog"
		platformField = project

		# TODO: Remove these in final run:
		#createdByField =  "ole.lynge.soerensen@schibsted.com"
		#assigneeField = None
		#collaborators = None

		csvwriter.writerow([title, descriptionField, assigneeField, collaborators, dueDate, section, subtaskOf, status, priority, issueType, createdByField, components, labelsField, jiraKey, createdField, platformField])


	with open(jiraCsvFileName, newline='') as f:
		reader = csv.reader(f)
		rowIndex = 0
		for row in reader:
			if rowIndex == 0:
				header = row
			cellIndex = 0
			for cell in row:
				if cell:
					log(str(cellIndex) + " / " + header[cellIndex] + ": " + cell[:50])
				cellIndex += 1
			if rowIndex > 0:
				mapAndWriteRow(row)
			rowIndex += 1
			if sampleSize > 0 and rowIndex > sampleSize: break
		print("Converted " + str(rowIndex) + " issues from " + jiraCsvFileName)

	asanaCsvfile.close()
	logFile.close()

def listUsers(jiraCsvFileName):
	def getValues(row, fieldName):
		return [value for index, value in enumerate(row) if value and header[index] == fieldName]

	def getValue(row, fieldName):
		values = getValues(row, fieldName)
		return "\n".join(values)

	def appendValue(input, row, fieldName):
		values = getValues(row, fieldName)
		if not values: return
		input.append("\n".join(values))

	def getWatchers(row):
		return [x for index, x in enumerate(row) if x and header[index] == "Watchers"]

	def getUsers(row):
		result = []
		appendValue(result, row, "Assignee")
		appendValue(result, row, "Reporter")
		appendValue(result, row, "Creator")
		return result + getWatchers(row)

	with open(jiraCsvFileName, newline='') as f:
		reader = csv.reader(f)
		rowIndex = 0
		users = []
		for row in reader:
			if rowIndex == 0:
				header = row
			else:
				users += getUsers(row)
			rowIndex += 1
		print("\n" + jiraCsvFileName + " :")
		print("Total usages: " + str(len(users)))
		counts = Counter(users)
		for user in counts:
			print(str(counts[user]) + " : " + user)
		#users = list(set(users))
		#users.sort()
		#for user in users:
		#	print(user)

convertJiraCsvToAsanaCsv("DBA-BST-2022-10-24.csv")
convertJiraCsvToAsanaCsv("Motors-BST-2022-10-24.csv")
#listUsers("Jira-DBA-2022.csv")
#listUsers("Jira-Motors-2022.csv")
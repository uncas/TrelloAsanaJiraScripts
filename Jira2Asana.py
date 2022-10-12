# Built on Python 3

# This script can assist in migrating a list of Jira tasks to Asana.

import csv
import glob
from datetime import datetime

# Set this to a positive number if you want to include only a few rows for testing:
# TODO: Set this to 0 when running with complete data:
sampleSize = 10

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
	csvwriter.writerow(['Name', 'Description', 'Assignee', 'Collaborators', 'Due Date', 'Section / Column', 'Subtask of', 'Status', 'Priority', 'Type', 'Reporter', 'Components', 'Labels', 'JiraKey', 'Created'])

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
		labels = ",".join(getValues(row, "Labels"))

		created = getValue(row, "Created")
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
		if labels: descriptionField += "\nLabels: " + labels
		if description: descriptionField += "\n\n" + description
		if comments: descriptionField += "\n\n" + comments

		reporterField = reporter if "@schibsted.com" in reporter else None
		assigneeField = assignee if "@schibsted.com" in assignee else None
		section = sprint if sprint else "Backlog"

		# TODO: Remove these in final run:
		reporterField =  "ole.lynge.soerensen@schibsted.com"
		assigneeField = None
		collaborators = None

		csvwriter.writerow([title, descriptionField, assigneeField, collaborators, dueDate, section, subtaskOf, status, priority, issueType, reporterField, components, labels, jiraKey, createdField])

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

	asanaCsvfile.close()
	logFile.close()

convertJiraCsvToAsanaCsv("DBA-BST.csv")
convertJiraCsvToAsanaCsv("Motors-BST.csv")
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

	def getComments(row):
		result = ""
		cellIndex = 0
		for cell in row:
			if cell:
				if header[cellIndex] == "Comment":
					result += "\n\nComment: " + cell
			cellIndex += 1
		return result

	def getCollaborators(row, people):
		watchers = [x for index, x in enumerate(row) if x and header[index] == "Watchers"]
		collaborators = set([x for x in people + watchers if "@schibsted.com" in x])
		return ",".join(collaborators)

	def concatIf(row, fromIndex, toIndex):
		result = ""
		hasValue = False
		for index in range(fromIndex, toIndex+1):
			value = row[index]
			if value:
				if hasValue:
					result += ","
				result += value
				hasValue = True
		return result

	asanaCsvFileName = "Asana-" + fileNameWithoutExtension + ".csv"
	asanaCsvfile = open(asanaCsvFileName, 'w')
	csvwriter = csv.writer(asanaCsvfile, dialect='excel')
	csvwriter.writerow(['Name', 'Description', 'Assignee', 'Collaborators', 'Due Date', 'Section / Column', 'Subtask of', 'Status', 'Priority', 'Type', 'Reporter', 'Components', 'Labels', 'JiraKey', 'Created'])

	def mapAndWriteRow(row):
		title = row[0]
		status = row[4]
		priority = row[11]
		issueType = row[3]
		sprint = row[222] if row[222] else row[243]
		dueDate = None
		subtaskOf = None
		assignee = row[13]
		jiraKey = row[1]
		components = concatIf(row, 23, 25)
		labels = concatIf(row, 28, 30)

		created = row[16]
		createdDate = datetime.strptime(created[:10], '%d.%m.%Y')
		createdField = datetime.strftime(createdDate, '%m/%d/%y')

		jiraLink = "https://jira.schibsted.io/browse/" + jiraKey
		reporter = row[14]
		creator = row[15]
		updated = row[17]
		description = row[31]
		comments = getComments(row)
		collaborators = getCollaborators(row, [reporter, creator])

		descriptionField = "Jira Link: " + jiraLink
		descriptionField += "\nReporter: " + reporter
		descriptionField += "\nCreator: " + creator
		descriptionField += "\nLast updated: " + updated
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
# Built on Python 3

# This script can assist in migrating a list of Jira tasks to Asana.

import csv
import glob
from datetime import datetime

def convertJiraCsvToAsanaCsv(jiraCsvFileName):
	fileNameWithoutExtension = jiraCsvFileName[:-5]
	logFileName = "Log - " + fileNameWithoutExtension + ".txt"
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

	def getCollaborators(row, reporter, creator):
		result = reporter + "," + creator
		cellIndex = 0
		for cell in row:
			if cell:
				if header[cellIndex] == "Watchers":
					result += "," + cell
			cellIndex += 1
		return result

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

	asanaCsvFileName = "Asana - " + fileNameWithoutExtension + ".csv"
	asanaCsvfile = open(asanaCsvFileName, 'w')
	csvwriter = csv.writer(asanaCsvfile, dialect='excel')
	csvwriter.writerow(['Name', 'Description', 'Assignee', 'Collaborators', 'Due Date', 'Section / Column', 'Subtask of', 'Status', 'Priority', 'Type', 'Reporter', 'Components', 'Labels'])

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
				title = row[0]

				status = row[4]
				priority = row[11]
				issueType = row[3]
				sprint = row[243]
				if row[222]: sprint = row[222]
				dueDate = None
				subtaskOf = None

				jiraKey = row[1]
				jiraLink = "https://jira.schibsted.io/browse/" + jiraKey
				reporter = row[14]
				created = row[16]
				updated = row[17]
				creator = row[15]

				description = "Jira Key: " + jiraKey 
				description += "\nJira Link: " + jiraLink
				description += "\nReporter: " + reporter
				description += "\nCreator: " + creator
				description += "\nCreated: " + created
				description += "\nUpdated: " + updated
				description += "\n\n"
				description += row[31] 
				description += "\n\n" + getComments(row)

				# TODO: INCLUDE THESE IN FINAL RUN:
				assignee = None #row[13]
				collaborators = None #getCollaborators(row, reporter, creator)

				components = concatIf(row, 23, 25)
				labels = concatIf(row, 28, 30)

				reporterUserName = reporter.replace("@schibsted.com", "")
				section = "Backlog"
				if sprint: section = sprint
				csvwriter.writerow([title, description, assignee, collaborators, dueDate, section, subtaskOf, status, priority, issueType, reporterUserName, components, labels])
			rowIndex += 1

	asanaCsvfile.close()
	logFile.close()

convertJiraCsvToAsanaCsv("DBA Platform B_ST 2.csv")
convertJiraCsvToAsanaCsv("Motors-BST.csv")
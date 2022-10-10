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

	asanaCsvFileName = "Asana - " + fileNameWithoutExtension + ".csv"
	asanaCsvfile = open(asanaCsvFileName, 'w')
	csvwriter = csv.writer(asanaCsvfile, dialect='excel')
	csvwriter.writerow(['Name', 'Description', 'Assignee', 'Collaborators', 'Due Date', 'Section / Column', 'Subtask of', 'Status', 'Priority', 'Type'])

	with open(jiraCsvFileName, newline='') as f:
		reader = csv.reader(f)
		rowIndex = 0
		for row in reader:
			if rowIndex == 0:
				header = row
			cellIndex = 0
			for cell in row:
				if cell:
					log(str(cellIndex) + " / " + header[cellIndex] + ": " + cell)
				cellIndex += 1
			if rowIndex > 0:
				title = row[0]

				status = row[4]
				priority = row[11]
				issueType = row[3]

				jiraKey = row[1]
				reporter = row[14]
				created = row[16]
				updated = row[17]
				creator = row[15]

				description = "Jira Key: " + jiraKey 
				description += "\nReporter: " + reporter
				description += "\nCreator: " + creator
				description += "\nCreated: " + created
				description += "\nUpdated: " + updated
				description += "\n\n"
				description += row[31] 
				description += "\n\n" + getComments(row)

				# TODO: INCLUDE THESE IN FINAL RUN:
				assignee = None #row[13]
				collaborators = None #reporter

				# TODO: Add 23+24+25 / Component/s
				#components = row[23]
				# TODO: Add 28+29+30 / Labels: Labels

				dueDate = None
				subtaskOf = None
				section = reporter.replace("@schibsted.com", "")
				csvwriter.writerow([title, description, assignee, collaborators, dueDate, section, subtaskOf, status, priority, issueType])
			rowIndex += 1

	asanaCsvfile.close()
	logFile.close()

convertJiraCsvToAsanaCsv("DBA Platform B_ST.csv")
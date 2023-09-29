import csv

def readTasks():
    result = []
    with open('Oles_tasks_schibstedcom.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            result.append(row)
    return result

def filterActiveTasks(tasks):
    result = []
    for task in tasks:
        assignee = task["Assignee"]
        completedAt = task["Completed At"]
        if not completedAt and assignee == "Ole Lynge Soerensen":
            result.append(task) 
    return result

def writeTasks(tasks):
    fieldNames = ['Name', 'Due Date', 'Tags', 'Notes']
    with open('Oles_active_tasks.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldNames)
        for task in tasks:
            def mapField(fieldName):
                return task[fieldName]
            values = map(mapField, fieldNames)
            writer.writerow(values)

def analyzeTasks(tasks):
    for task in tasks:
        if task["Note"]:
            print(task["Note"])

tasks = readTasks()

print(len(tasks))

activeTasks = filterActiveTasks(tasks)

print(len(activeTasks))
print(activeTasks[0])

writeTasks(activeTasks)
import csv

def readTasks():
    result = []
    with open('_Weekly_Promises_.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            result.append(row)
    return result

def filterActiveTasks(tasks):
    result = []
    for task in tasks:
        completedAt = task["Completed At"]
        if not completedAt:
            result.append(task) 
    return result

def writeTasks(tasks):
    fieldNamesToMap = ['Name', 'Due Date', 'Tags', 'Notes', '\ufeffTask ID', 'Parent task', 'Assignee Email', 'Section/Column']
    fieldNames = fieldNamesToMap.copy()
    fieldNames.append('Parent ID')
    fieldNames.append('Task Type')
    with open('Balance_active_tasks.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldNames)
        for task in tasks:
            def mapField(fieldName):
                return task[fieldName]
            values = list(map(mapField, fieldNamesToMap))
            taskType = 'Task'
            parentId = None
            if task['Parent task']:
                taskType = 'Subtask'
                parentTask = [x for x in tasks if x['Name'] == task['Parent task']]
                if (parentTask):
                    parentId = parentTask[0]['\ufeffTask ID']
            values.append(parentId)
            values.append(taskType)
            if taskType == 'Task':
                writer.writerow(values)
                print(task['Name'])

def analyzeTasks(tasks):
    for task in tasks:
        if task["Note"]:
            print(task["Note"])

tasks = readTasks()

print("All tasks: ", len(tasks))
#print(tasks[0])

activeTasks = filterActiveTasks(tasks)

print("Active tasks: ", len(activeTasks))
#print(activeTasks[0])

writeTasks(activeTasks)
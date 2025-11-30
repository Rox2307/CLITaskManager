tasks = []
loaded_tasks = []


exit_program = False
autosave = False

id_count = 0

commands_parameters = {'add':['title', 'deadline', 'description','priority', 'status', 'tags'],
            'list':'0',
            'delete':'id',
            'update':['title', 'deadline', 'description','priority', 'status', 'tags', 'id'],
            'search':['priority', 'status', 'deadline', 'tags'],
            'save':"0",
            'load':"0", 
            'exit':"0",
            'autosave': "0"}
commands = ['add', 'list', 'delete', 'update', 'search', 'save', 'load', 'exit', 'autosave']

def get_index_from_id(id):
    i=0
    for task in tasks:
        if int(task["id"]) == id:
            return i
        else:
            i += 1
    return -1

def parse_inputs(input):
    return input.rsplit(" ")
def save():
    global loaded_tasks
    with open("tasks.txt", "w") as file:
            file.write(str(tasks))

def execute_command(command, parameters):
    global exit_program
    global tasks
    global id_count
    global loaded_tasks
    global autosave
    for parameter, _ in parameters:
        if parameter in commands_parameters[command]:
            continue
        else:
            print("These arguments don't exist.")
            return 0
        

    if command == "add":
        id_count += 1
        new_task = dict(parameters)
        new_task["id"] = id_count
        if "title" not in new_task:
            print("Title is required.")
            return 0
        if "status" in new_task:
            if not((new_task["status"] == "todo") or (new_task["status"] == "doing") or (new_task["status"] == "done")):
                print("Invalid status.")
                return 0
        tasks.append(new_task)
        
        print(new_task)
        if autosave == True:
            save()


    elif command == "list":
        if not tasks:
            print("There are no tasks.")
            return 0
        i = 1
        print("Task {}:".format(i))
        for task in tasks:
            for parameter in task:
                print(parameter + ": " + str(task[parameter]))
            print("____________________")
            i += 1
        
    

    elif command == "delete":
        #print(parameters)
        id = int(parameters[0][1])
        if get_index_from_id(id) == -1:
            print("That task doesn't exist")
            return 0
        else:
            index=get_index_from_id(id)
        tasks.pop(index)
        print("Task deleted")
        if autosave == True:
            save()
    

    elif command == "update":
        updated_task = dict(parameters)
        if int(get_index_from_id(int(updated_task['id']))) == -1:
            print("That task doesn't exist")
            return 0
        else:
            task_id = int(get_index_from_id(updated_task['id']))
            task_toupdate = tasks[task_id]
        for parameter in updated_task:
            task_toupdate[parameter] = updated_task[parameter]
        if autosave == True:
            save()

    

    elif command == "search":
        search_filters = dict(parameters)
        filtered_tasks = []
        

        for filter in search_filters:
            i = 0
            for task in tasks:
                if task[filter] == search_filters[filter]:
                    filtered_tasks.append(i)
                i += 1
        not_reapeated_tasks = []
        if not filtered_tasks:
            print("No tasks match your description")
            return 0
        for index in filtered_tasks:
            if index not in not_reapeated_tasks:
                not_reapeated_tasks.append(index)
        
        else:
            i = 1
            print(not_reapeated_tasks)
            for task_index in not_reapeated_tasks:                
                print("Task {}:".format(i))
                tasks_index = tasks[task_index]
                for parameter in tasks_index:
                    print(parameter + ": " + str(tasks_index[parameter]))
                print("____________________")
                i += 1
        return 0
    
    elif command == "save":
        save()
    elif command == "load":
        with open("tasks.txt") as file:
            loaded_tasks = eval(file.read())
        if not loaded_tasks:
            print("There are no saved tasks.")
            return 0
        i = 1
        print("Task {}:".format(i))
        for task in loaded_tasks:
            task
            for parameter in task:
                print(parameter + ": " + str(task[parameter]))
            print("____________________")
            i += 1

    elif command == "autosave":     
        if autosave == True:
            autosave = False
        autosave = True
        

    elif command == "exit":
        print("exiting program")
        exit_program = True
        return
    
def process_input(input):
    arguments = []
    parsed_input = parse_inputs(input)
    if parsed_input[0] not in commands:
        print("Not a command, try again")
    else:
        command_used = parsed_input[0]
        parsed_input.pop(0)
        if parsed_input == ['']:
            execute_command(command_used, [["0", "0"]])
        else:
            for i in parsed_input:
                temp_args=[]
                parsed_args = i.rsplit("=")
                if "=" not in i:
                    print("Not a valid parameter, try again")
                    return 0
                for j in parsed_args:
                    temp_args.append(j)
                    #print(j)
                arguments.append(temp_args)
            #print("Arguments:")
            #print(arguments)
            execute_command(command_used, arguments)


while not exit_program:
    command_input = str(input(">"))
    if " " not in command_input:
        command_input += " "
    process_input(command_input)
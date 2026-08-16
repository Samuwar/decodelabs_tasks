######### TO DO LIST ###########
import json
import time
from datetime import datetime

CLEAR = "\033[2J"   #this clears the screen // print(CLEAR)
file_path = "to_do.json"    # File path of the file to record task on local desktop

#Open the file to read and save tasks and if it doesn't exist, create the file
try: 
    with open(file_path, 'r', encoding="utf-8") as file: 
        data = json.load(file)
except FileNotFoundError:
    data = {"data": []}
    with open(file_path, 'w') as file:
        json.dump(data, file)

my_task = data['data']

def add_task():
    """Add New Task"""
    print(CLEAR)
    print("Add Task".center(20), end="\n\n")    #Header for display
    task = input("Enter task to do: ")      # Task to be added
    
    # My Schema is {task, date_added, completed, date_completed}
    my_task.append({"Task":task,"Date_added":datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "Completed":"No", "Date_completed":""})
    print(CLEAR)
    print(f"{task} is added successfully!")
    input("Press Enter key to go to main menu ")   
    return True

def view_task(task_list, not_completed=True):
    """View uncompleted Tasks"""
    #Task list is either completed list or uncompleted list sent from the main menu
    #not_completed = True for view_task()
    #not_completed = False for completed_task()
    print(CLEAR)
    
    # Loop until the input is acceptable
    while True:
        if not_completed:       #To do tasks
            print("To Do List:".center(80))
            print("{:<5}".format("S/N"), "{:<32}".format("| TASK"),"{:<12}".format('| COMPLETED'), "{:<24}".format("| DATE ADDED")) #Header
            for index, item in enumerate(task_list):
                print("-"*80)       #Print line to divide item rows
                print("{:<5}".format(index+1), "{:<32}".format("| " + item.get('Task')), "{:<12}".format("| "+item.get('Completed')), "{:<24}".format("| " + item.get('Date_added')))       # Print items and format them 
        else:       #Completed Tasks
            print("Completed Tasks:".center(98))
            print("{:<5}".format("S/N"), "{:<32}".format("| TASK"),"{:<12}".format('| COMPLETED'), "{:<24}".format("| DATE ADDED"), "{:<24}".format("| DATE COMPLETED"))        # Header
            for index, item in enumerate(task_list):
                print("-"*98)       # Print line to divide items into rows
                print("{:<5}".format(index+1), "{:<32}".format("| " + item.get('Task')), "{:<12}".format("| "+item.get('Completed')), "{:<24}".format("| " + item.get('Date_added')), "{:<24}".format("| " + item.get('Date_completed')))       # Print items and format them
            
        print("\n\nselect a task to mark as completed or 0. Return to main menu")
        try:
            option = int(input("Select an item: "))     # Select task to mark
            if option == 0: return
            else:
                option = option - 1  
                print(CLEAR)
                print(f"{task_list[option]['Task']}\n")
                break
        except ValueError: print("Only number is allowed\n")
        except IndexError: print("Select a number from the list")  
          
    #ADD FUNCTION TO DELETE TASK: SELECT TASK, THEN MARK OR DELETE TASK
    while True:
        try:
            if not_completed:       # For to do task
                option1 = int(input("1. Mark Task as Done \n2. Delete Task \n0. Return to Main Menu: "))    # Select task to mark or delete
                if option1 == 1:
                    task_list[option]['Completed'] = "Yes"
                    task_list[option]['Date_completed'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    break
                elif option1 == 2:
                    my_task.remove(task_list[option])
                    break
                else: return
            else:       # For completed tasks
                option1 = int(input("1. Delete Task \n0. Return to Main Menu: "))
                if option1 == 1:
                    my_task.remove(task_list[option])
                    break
                else: return
        except ValueError: print("Only number is allowed\n\n\n")
        
def main():
    """Main Menu"""
    print(CLEAR)
    print("Main Menu\n\n1. Add Task \n2. View Task \n3. Completed Task \n0. Quit")
    to_do_task = [x for x in my_task if x['Completed'] == "No"]
    completed_task = [x for x in my_task if x['Completed'] == "Yes"]
    try:
        option = int(input("Select an option: "))
        match option:
            case 1: add_task()
            case 2: view_task(to_do_task)
            case 3: view_task(completed_task, False)
            case _: return False
    except ValueError: print("Only numbers is allowed")
    return True

while True:     # Keep running the programme until you quit
    if main() == False:
        print("Ending Program ...")
        time.sleep(.5)
        print(CLEAR)
        break
    data_string = json.dumps(data, indent=4)
    with open(file_path, 'w') as file:
        file.write(data_string)   
   
######### TO DO LIST ###########
import json
import time

my_task = []
completed_task = []

def add_task():
    task = input("Enter task to do: ")
    my_task.append({'Task':task,'Date':time.ctime(), "Completed":'No'})
    print(json.dumps(my_task), end="\n\n\n\n\n")
    return

def view_task():
    print("To Do List:")
    for index, item in enumerate(my_task):
        print(f"{index+1}. {item}")
    print("0. Return to main menu")
    not_acceptable = True
    while not_acceptable:
        try:
            option = int(input("Select an item: "))-1
            if option == -1: return
            print(my_task[option],"\n\n1. Mark as done \n0. Return to Main Menu")
            not_acceptable = False
        except ValueError: print("Only number is allowed\n\n\n")
        except IndexError: print("Select a number from the list")    
    
    not_acceptable = True
    while not_acceptable:
        try:
            option = int(input("Select an Option: "))
            if option == 1:
                my_task[option]['Completed'] = "Yes"
                not_acceptable = False
            else: return
        except ValueError: print("Only number is allowed\n\n\n")
        except IndexError: print("Select a number from the list")    
    return

def completed_task():
    print("Completed Task:\n\n")
    for index, item in enumerate(completed_task):
        print(f"{index+1}. {item}")
    return


def main():
    print("Main Menu\n\n1. Add Task \n2. View Task \n3. Completed Task")
    try:
        option = int(input("Select an option: "))
        match option:
            case 1: add_task()
            case 2: view_task()
            case 3: completed_task()
            case _: return False
    except ValueError: print("Only numbers is allowed")
    return True

run = True
while run:
   run = main()
   print("Returning to Main Menu...")
   time.sleep(2)
       
   



#EXPENSE TRACKER
# ADD EXPENSE
# VIEW TOTAL EXPENSE
# MENU
import time
import json

CLEAR = "\033[2J"       #this clears the screen // print(CLEAR)
file_path = "expense_tracker.json"      # File path of the file to record expense on local desktop

#Open the file to read and save tasks and if it doesn't exist, create the file
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {"data": []}
    with open(file_path, 'w') as file:
        json.dump(data, file)
expense_list = data["data"]

def add_expense():
    print(CLEAR)
    print("ADD EXPENSE".center(20), end="\n\n")     #Header for display
    item = input("Enter Expense Item: ")        # Expense Item
    while True:     # Loop until input is acceptable, Input must be integer
        try:
            price = int(input("Enter Expense Amount: "))
            break
        except ValueError: print("\n\n\nOnly Number is allowed\n\n")       
    expense = {"item":item, "price":price, "date":time.ctime()}     # Add item, price and date together in a dict
    expense_list.append(expense)        # Add the expense to the expense list
    view_expense(True)      # Call view_expense(True), True -> Displays the expense list for only 2 seconds and then return to main menu
    return True


def view_expense(add=False):
    """View Expense List: """
    print(CLEAR)
    print("EXPENSE LIST".center(50))        # Title
    print("{:<5}".format("S/N"), "{:<28}".format("| ITEM"), " {:<10}".format("| PRICE"), "{:<12}".format("| DATE"))     #Headers
    total_expense = 0       # Initial total
    for index, item in enumerate(expense_list):
        print("-"*73)       # Divides the rows
        print("{:<5}".format(index+1), "{:<29}".format("| "+ item.get("item")), "{:<10}".format("| "+ str(item.get("price"))), "{:<12}".format("| " +item.get("date")))     # Print the expense item, price and date and format them
        total_expense+=item.get("price")        # Add price of item to initial total
    print()     # Print empty space
    print("{:>23}".format("TOTAL EXPENSE: "), "{:>17}".format(total_expense))   # Print total expense under
     
    if add == False:        # if view_expense is called from main menu
        while True:
            try:
                option = int(input("\n\nSelect item to delete \n0. Main Menu: ")) - 1
                if option <= -1: return
                else:
                    if input(f"\n\nAre you sure you want to delete this {expense_list[option]['item']} {expense_list[option]['price']}? (y/n): ").lower().strip() == 'y':
                        item_name = expense_list[option]['item']
                        expense_list.remove(expense_list[option])       # remove item from expense list
                        input(f"{item_name} is deleted successfully \n\nPress Enter Key to continue to main menu: ")
                    break
            except ValueError: print("Only Number is allowed")
            except IndexError: print("Select a number from the list of items")       
    else:       # Go to Main menu after 2 seconds
        print("\n\n Main Menu Loading...")
        time.sleep(2) 
    print(CLEAR)
    return True

def main_menu():
    print(CLEAR)
    print("MAIN MENU\n".center(15))     # print title
    while True:     # Loops until input is acceptable
        try:        # handle error if input is not integer
            option = int(input("1. ADD EXPENSE\n2. VIEW EXPENSES LIST \n0. QUIT\n\nSelect an option: "))
            break
        except ValueError: print("\n\n\nOnly Number is allowed\n")
    if option == 1: return add_expense()    # if user inputs 1, go to add expense
    elif option == 2: return view_expense()     # if user input = 2, go to view expense
    else:       # if user input is not 1 or 2, quit programme
        print(CLEAR)
        print("Ending Program...")
        time.sleep(.5)
        print("Program ended\n\n\n")
        return False
        
while True:
    if main_menu() == False: break
        
    data_string = json.dumps(data, indent=4)
    with open(file_path, 'w') as file:
        file.write(data_string)
    
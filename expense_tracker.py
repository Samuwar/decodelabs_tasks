#EXPENSE TRACKER
# ADD EXPENSE
# VIEW TOTAL EXPENSE
# MENU
import time
CLEAR = "\033[2J"
expense_list = []
def add_expense():
    print(CLEAR)
    print("ADD EXPENSE".center(20), end="\n")
    item = input("Enter Expense Item: ")
    not_acceptable = True
    while not_acceptable:
        try:
            price = int(input("Enter Expense Amount: "))
            not_acceptable = False
        except ValueError: print("\n\n\nOnly Number is allowed\n\n")       
    expense = {"item":item, "price":price, "date":time.ctime()}
    expense_list.append(expense)
    view_expense(True)
    return True


def view_expense(add=False):
    print(CLEAR)
    print("Expense List".center(50))
    print("{:<5}".format("S/N"), "{:<28}".format("| ITEM"), " {:<10}".format("| PRICE"), "{:<12}".format("| DATE"))
    total_expense = 0
    for index, item in enumerate(expense_list):
        print("-"*73)
        print("{:<5}".format(index+1), "{:<29}".format("| "+ item.get("item")), "{:<10}".format("| "+ str(item.get("price"))), "{:<12}".format("| " +item.get("date")))
        total_expense+=item.get("price")
    print("{:>23}".format("TOTAL EXPENSE: "), "{:>17}".format(total_expense)) 
    if add == False: input("\n\nPress Enter key to go to Main Menu: ")
    else:
        print("\n\n Main Menu Loading...")
        time.sleep(2) 
    print(CLEAR)
    return True
    
def main_menu():
    print(CLEAR)
    print("MAIN MENU\n".center(15))
    not_acceptable = True
    while not_acceptable:
        try:
            option = int(input("1. ADD EXPENSE\n2. VIEW EXPENSES LIST \n0. QUIT\n\nSelect an option: "))
            not_acceptable = False
        except ValueError: print("\n\n\nOnly Number is allowed\n")
    if option == 1: return add_expense()
    elif option == 2: return view_expense()
    else:
        print(CLEAR)
        print("Ending Program...")
        time.sleep(.5)
        print("Program ended\n\n\n")
        return False
        
run = True
while run:
    run = main_menu()
    
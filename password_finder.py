import string
import random
import getpass
import time

CLEAR = "\033[2J"
CLEAR_LINE = "\033[H"
password_char = ''.join([string.ascii_letters, string.digits, string.punctuation])

def find_password():
    password = getpass.getpass("Enter Password: ", echo_char='*')
    password_length = len(password)
    generated_password = ''.join(random.choices(password_char, k=4))
    print(CLEAR)
    start_time = time.perf_counter()
    while True:
        generated_password = ''.join(random.choices(password_char, k=password_length))
        print(CLEAR_LINE)
        print(generated_password)
        if password == generated_password:
            end_time = time.perf_counter()
            print(f"Password is: {generated_password}")
            print(f"total time taken: {end_time - start_time:.4f} seconds")
            break
        
def find_password2():
    password = getpass.getpass("Enter Password: ", echo_char='*')
    password_length = len(password)
    matched_password = ''
    
    print(CLEAR)
    start_time = time.perf_counter()
    for char in password:
        if char in password_char:
            matched_password = ''.join([matched_password, char])
            
    print(matched_password)
    end_time = time.perf_counter()
    print(f"total time taken: {end_time - start_time:.4f} seconds")

find_password2()
    
########## PASSWORD GENERATOR ############
import string
import secrets
import random

unwanted_characters = ["`", '"', '>','<', '\\']
password_chars = [x for x in ''.join([string.ascii_letters, string.digits, string.punctuation]) if x not in unwanted_characters]
password_length = random.randrange(15, 62)
password = ''
for i in range(0, password_length):
    password = ''.join([password, secrets.choice(password_chars)])

print(f"Password: {password}\nPassword Length: {len(password)}")
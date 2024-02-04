"""
Deliverable 2
Jason Xie
xix277
11255431


"""


from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("key.txt", 'wb') as f:
    f.write(key)

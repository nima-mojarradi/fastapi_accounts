import hashlib

def hash_password(password:str):
    return hashlib.md5(bytes(password,'utf-8')).hexdigest()

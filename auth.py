import bcrypt 
import json 
import os 
import getpass

CONFIG_FILE = "config.json"

def _load_config() :
    if not os.path.exists(CONFIG_FILE):
        return {}

    if os.path.getsize(CONFIG_FILE) == 0:
        return {}

    if not os.path.exists(CONFIG_FILE) :
        return {}
    with open(CONFIG_FILE,"r") as file :
        return json.load(file)

def _save_config(data) :
    with open(CONFIG_FILE , "w") as file :
        json.dump(data , file , indent=4)

def is_master_password_set() :
    # Check master password by user set or not !
    config = _load_config() 
    return "password_hash" in config

def setup_master_password() :
    ''' Steps are : 
    1. First user will create a master password.
    2. We will hash the password using the bcrypt.
    3. Only store the hash.
    '''    
    print("SETUP MASTER PASSWORD")
    print("If you forgot this password , your vault can't be recovered back ! ")
    while True: 
        password = getpass.getpass("Create master password")
        confirm = getpass.getpass("Confirm master password")
        if password != confirm :
            print("Password should match.")
            continue
        if len(password) < 8 :
            print("Length of password must be atleast 8 long.")
            continue
        break 
    password_hash = bcrypt.hashpw(
        password.encode("utf-8") , 
        bcrypt.gensalt(rounds=15)
    ).decode("utf-8") 
    
    config = {
        "password_hash" : password_hash
    }
    
    _save_config(config)
    
    print("Master password set up successfully !")
    
def verify_master_password() :
    # Verifying user entered password (True for correct else False !)
    config = _load_config() 
    if "password_hash" not in config : 
        print("Master password not set.")
        return False 
    stored_hash = config["password_hash"].encode("utf-8")
    password = getpass.getpass("Enter master password : ")
    
    if bcrypt.checkpw(password.encode("utf-8") , stored_hash) :
        print("Access granted !")
        return True    
    print("Incorrect password") 
    return False 
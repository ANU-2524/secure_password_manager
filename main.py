from auth import is_master_password_set , setup_master_password, verify_master_password
from kdf import derive_key
from vault import add_credential, get_credential, delete_credential, list_services
from generator import generate_password
from clipboard import copy_with_timeout
import getpass


def main():
    if not is_master_password_set():
        setup_master_password()

    if not verify_master_password():
        return

    master_pwd = getpass.getpass("Enter master password again: ")
    key = derive_key(master_pwd)

    while True:
        print("\n1. Add credential")
        print("2. Get credential")
        print("3. Delete credential")
        print("4. List services")
        print("5. Generate password")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            s = input("Service: ")
            u = input("Username: ")
            p = getpass.getpass("Password: ")
            add_credential(s, u, p, key)
            print("Saved.")

        elif choice == "2":
            s = input("Service: ")
            cred = get_credential(s, key)
            if not cred:
                print("Not found.")
            else:
                print("Username:", cred["username"])
                copy_with_timeout(cred["password"])
                print("Password copied to clipboard (10s).")

        elif choice == "3":
            s = input("Service: ")
            delete_credential(s)
            print("Deleted.")

        elif choice == "4":
            print("Services:", list_services())

        elif choice == "5":
            length = int(input("Length: "))
            print("Generated:", generate_password(length))

        elif choice == "6":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

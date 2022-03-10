import csv
from create_files import getting_users
class User:

    # users (default user = admin)
    def __init__(self):
        self.users = getting_users()

    def register(self):
        """
        Adds new member information to users collection and updates the "user_info.csv" file
        """
        while True:
            name = input("Create a username: ").strip()
            if name in self.users.keys():
                print("Username already exists! Please enter a different username...")
                continue

            password = input("Create a password: ").strip()
            break

        #Adding user name as key, password for values to the user dictionary
        self.users[name] = {"password": password}

        #Appending new user to the user dictionary
        try:
            with open("user_info.csv", "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, self.users[name]["password"]])
        except PermissionError as e:
            print(f"Please make sure your csv file is closed on your system. {e}")
            exit(0)

        print(f"You registered {name}!")
        print("Please login")

        return self.login()

    def login(self):
        """
        Authentication function

        Returns:
            str: username
        """
        while True:
            name = input("Please enter your username: ").strip()
            password = input("Please enter your password: ").strip()
            
            if name not in self.users.keys() or password != self.users[name]["password"]:
                print("Username or password is wrong! Please try again.")
                continue
            else:
                print("You're logged in!")
                break

        return name
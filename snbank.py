# list of modules to be used
import json
from datetime import datetime
import random
import os

# list of variables to be used
staffExists = False
closeApp = False
closeStaffLogin = False

# Open up staff.txt and read the data into a variable we can use
with open("staff.txt", "r+") as file:
    staffdatabase = json.load(file)


def doesStaffExists(getUsername, getPassword):
    # it iterates through the staff database and checks if staff exists
    # if yes, it returns True and some other parameters we need for the session file
    for key in staffdatabase.keys():
        # print(key)
        if getUsername == staffdatabase[key]["Username"] and getPassword == staffdatabase[key]["Password"]:
            staffExists = True
            return staffExists, staffdatabase[key]["Full Name"], staffdatabase[key]["Username"], staffdatabase[key]["Email"]

    # if staff does not exist, return False
    print("Staff does not Exist")
    staffExists = False
    return staffExists, None, None, None


def createNewCustomerAccount():
    # Firstly, it creates a random 10 digit Account number while ensuring it begins with 00 (like normal banks)

    rand = random.randint(10000000, 99999999)
    randomNumber = "00" + str(rand)

    #  then staff takes note of Customer details

    print(f"\n******** To Create new Bank Account, Fill the Form below ********\n")
    customerName = input("Enter Customer Name: ")
    customerOpeningBalance = input("Enter Customer's opening Balance: $")
    typeOfCustomerAccount = input(
        "Preferred customer account. Savings/Current/Fixed: ")
    customerAccountEmail = input("Enter Customer Account Email: ")

    # then the customer file is opened so the list of customers can be read
    with open("customer.txt", "r") as file:
        customerDatabase = json.load(file)

    # this ensures the customer details is added to the end of the customer database
    getListOfKeys = list(customerDatabase.keys())
    getLastKey = getListOfKeys[-1]
    getNewKey = int(getLastKey) + 1

    # the customer database is updated with user information
    customerDatabase[getNewKey] = {
        "Account Name": customerName,
        "Type of Account": typeOfCustomerAccount,
        "Account Email": customerAccountEmail,
        "Current Balance": customerOpeningBalance,
        "Account Number": randomNumber
    }

    # then the updated customer database is written back to customer.txt

    with open("customer.txt", "w+") as file:
        file.write(json.dumps(customerDatabase))

    # the generated Account Number is displayed to the staff
    print(f"\n************************************")
    print(f"The generated Account Number for the Customer is {randomNumber} ")
    print(f"\n************************************\n")


def checkCustomerAccountDetails():
    # asks staff to input account number of user
    getCustomerAccountNumber = input("Enter the Account Number of Customer: ")

    # then it opens the customer.txt file so the customer details can be read
    with open("customer.txt", "r+") as file:
        customerDatabase = json.load(file)

    # if the inputed account number matches any customer account in the database, then the customer details are displayed
    for key in customerDatabase.keys():
        if getCustomerAccountNumber == customerDatabase[key]["Account Number"]:
            print(
                f"\n***************\n The Customer Account details is:\n {customerDatabase[key]}\n***************")
            return
    print(
        f"\n ************* Oooppss!, Sorry, Customer does not Exist, Try again! ***********")


def staffLogout():

    # checks if session file exists then deletes it, also watches out for errors

    if os.path.exists("session.txt"):
        try:
            os.remove("session.txt")
        except OSError as err:
            print(f"exception handled: {err}")
    else:
        print("The File does not exist.")


# ******************** Start from Here *************************
#  while loop that keeps repeating
# Asks if Staff wants to login or to close app(stops while loop)

while closeApp == False:

    print(f"*************Welcome to snBank************** \n \n What would you like to do? \n  1: Staff Login \n  2: Close App \n")
    reply = input("Select Option: ")

    # if staff wants to login
    if int(reply) == 1:
        print(f"*************** Welcome ****************\n")
        getUsername = input("Please enter your Staff Username: ")
        getPassword = input("Please enter your Staff Password: ")

        # check if staff exists by calling doesStaffExist()
        staffExists, staffName, staffUsername, staffEmail = doesStaffExists(
            getUsername, getPassword)

        # if staff Exists
        if staffExists == True:

            # generate a session file and record the data of staff then print it
            dateAndTime = datetime.now()
            sessionFile = open("session.txt", "w+")
            sessionFile.write(f"Staff Name: {staffName} \n")
            sessionFile.write(f"Staff Username: {staffUsername} \n")
            sessionFile.write(f"Staff Email: {staffEmail} \n")
            sessionFile.write(f"Date and Time of Login: {dateAndTime}")
            sessionFile.close()

            sessionFile = open("session.txt", "r+")
            print(
                f"\n********The current Staff session is******** \n{sessionFile.read()}")
            sessionFile.close()

        # then it creates a while loop to which displays Staff DashBoard

            while closeStaffLogin == False:

                print(f"\n ****************************************")
                print(f"Welcome User, What would you like to do?\n 1: Create new Bank Account\n 2: Check Customer Account Details\n 3: Logout")
                print(f"****************************************\n")

                reply = input("Select Option?: ")

                # if staff wants to create an account, call create new account function

                if int(reply) == 1:
                    createNewCustomerAccount()
                # if staff wants to check customer details, we run the function below
                elif int(reply) == 2:
                    checkCustomerAccountDetails()
                # if the staff wants to logout, the function is called and the while loop is terminated
                elif int(reply) == 3:
                    staffLogout()
                    closeStaffLogin = True

        # if staff doesnt Exist, the staff is asked to try again

        else:
            print(
                f"*************************\n Ooopss!!! Please try again \n********************************")

    # if USer wants to closeApp, then the while loop is terminated and the script terminates

    elif int(reply) == 2:
        print(f"\n*************** Goodbye User! *****************\n")
        closeApp = True

##############################
#           Imports          #
##############################
from guizero import App, Window, Text, PushButton, TextBox, info, Box, ButtonGroup, Picture, CheckBox, ListBox
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
import sqlite3
from datetime import datetime, timedelta
import base64
import os
import os.path
#####################
#     Constants     #
#####################
database_file = "RetailTracking.db"
global_image_location = 'matplotlib_images/'
image_location1 = f'{global_image_location}Graph1.png'
image_location2 = f'{global_image_location}Graph2.png'
image_location3 = f'{global_image_location}Graph3.png'
image_location4 = f'{global_image_location}Graph4.png'
GraphSize = 450
Evens = [0,2,4]
Odds = [1,3,5]
count = 0
###############################################
#                Database Setup               #
#                                             #
#           Delete Existing Database          #
###############################################
# This function deletes a database.
# checks if file exist if it does then it removes it
def delete_database(database_file):
    if os.path.exists(database_file):
        os.remove(database_file)
#######################################################
#              Executing SQL in a File                #
#######################################################
def init_db(database_file, database_sql):   
    # open the sqlite database file
    conn = sqlite3.connect(database_file)
    # connect to it and get a cursor
    # this is like a placeholder in the database
    cursor = conn.cursor()                  
    # open the script file containing SQL
    script = open(database_sql, 'r')
    # read the contents of the script 
    # into a string called sql
    sql = script.read()                     
    # execute the SQL 
    cursor.executescript(sql)               
    # commit the changes to make them permanent
    conn.commit()                           
    # close the connection to the database
    conn.close() 
#############################################
#              Executing SQL                #
#############################################
def Insert_Data(database_file, sql):   
    # open the sqlite database file
    conn = sqlite3.connect(database_file)
    # connect to it and get a cursor
    # this is like a placeholder in the database
    cursor = conn.cursor()                  
    cursor.executescript(sql)               
    # commit the changes to make them permanent
    conn.commit()                           
    # close the connection to the database
    conn.close()

########################################
#          Query the Database          #
########################################
# this peice of code connected to the database file i have in my files
# it then creates a variable to hold all the data and uses cursor function
# it then excecutes the sql code its give and returns all the rows that it found
def query_database(database, query):
    # this is used to pass a query and then it will fetchall rows found and then return this value
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows
##############################################
#          Message Certain Customer          #
##############################################
def MessageThatCustomer():
    global EmployeeID
    global CustomerID
    global CustomerFullName
    CustomerFullName = CustomerListbox.value
    CustomerNameArray = CustomerFullName.split(" ")
    CustomerFirstName = CustomerNameArray[0]
    CustomerSecondName = CustomerNameArray[1]
    query = ("SELECT * FROM Customer_Table WHERE Forename = '" + CustomerFirstName + "' AND Surname = '"+ CustomerSecondName + "'")
    print(query)
    EmployeeMessage1.value = ""
    EmployeeMessage2.value = ""
    EmployeeMessage3.value = ""
    CustomerMessage1.value = ""
    CustomerMessage2.value = ""
    MessageTextbox.value = ""
    row = query_database(database_file, query)
    CustomerID = row[0][0]
    EmployeeMessagingPage.show()
    EmployeeCustomersPage.hide()
    query = ("SELECT * FROM Message_Table WHERE CustomerID = " + str(CustomerID) + " AND EmployeeID = " + str(EmployeeID) + " ORDER BY MessageID ASC LIMIT 5")
    print(query)
    row = query_database(database_file, query)
    for x in range(0, len(row)):
        if x in Evens:
            if x == 0:
                EmployeeMessage1.value = row[x][5] + "\n - From " + row[x][3]
            elif x == 2: 
                EmployeeMessage2.value = row[x][5] + "\n - From " + row[x][3]
            else:
                EmployeeMessage3.value = row[x][5] + "\n - From " + row[x][3]
        elif x in Odds:
            if x == 1:
                CustomerMessage1.value = row[x][5] + "\n - From " + row[x][3]
            elif x == 3:
                CustomerMessage2.value = row[x][5] + "\n - From " + row[x][3]
                

##################################
#          Send Message          #
##################################

def CustomerViewMessages():
    global CustomerID
    global EmployeeID
    CEmployeeMessage1.value = ""
    CEmployeeMessage2.value = ""
    CEmployeeMessage3.value = ""
    CCustomerMessage1.value = ""
    CCustomerMessage2.value = ""
    CustomerMessageTextbox.value = ""
    query = ("SELECT * FROM Message_Table WHERE CustomerID = " + str(CustomerID) + " ORDER BY MessageID ASC LIMIT 5")
    print(query)
    row = query_database(database_file, query)
    if row == []:
        CustomerProductsPage.show()
        CustomerMessagingPage.hide()
        info("Error", "There is no message from an employee")
        return
    EmployeeID = row[0][2]
    for x in range(0, len(row)):
        if x in Evens:
            if x == 0:
                CEmployeeMessage1.value = row[x][5] + "\n - From " + row[x][3]
            elif x == 2: 
                CEmployeeMessage2.value = row[x][5] + "\n - From " + row[x][3]
            else:
                CEmployeeMessage3.value = row[x][5] + "\n - From " + row[x][3]
        elif x in Odds:
            if x == 1:
                CCustomerMessage1.value = row[x][5] + "\n - From " + row[x][3]
            elif x == 3:
                CCustomerMessage2.value = row[x][5] + "\n - From " + row[x][3]

def CustomerSendMessage():
        global CustomerID
        global EmployeeID
        global CustomerFullName
        MessageText = CustomerMessageTextbox.value
        if MessageText == "":
            info("Error", "You didnt enter a message in the textbox.")
            return
        query = ("SELECT * FROM Employee_Table WHERE EmployeeID = " + str(EmployeeID))
        print(query)
        row = query_database(database_file, query)
        EmployeeFullName = row[0][3] + " " + row[0][4]
        now = datetime.now()
        formatted_now = now.strftime("%Y/%m/%d/%H/%M/%S")
        InsertSQL = ("INSERT INTO Message_Table(CustomerID, EmployeeID, FromName, ToName, MessageText, Product, Timestamp) VALUES(" + str(CustomerID) + ", " + str(EmployeeID) + ", '"+ str(CustomerFullName) + "', '" + str(EmployeeFullName) + "', '" + str(MessageText) + "', 'PS5', '" + str(formatted_now) + "')")
        print(InsertSQL)
        Insert_Data(database_file, InsertSQL)
        CustomerViewMessages()


def EmployeeSendMessage():
    MessageText = MessageTextbox.value
    if MessageText == "":
        info("Error", "You didnt enter a message in the textbox.")
        return
    global CustomerID
    global EmployeeID
    global CustomerFullName
    query = ("SELECT * FROM Employee_Table WHERE EmployeeID = " + str(EmployeeID))
    print(query)
    row = query_database(database_file, query)
    EmployeeFullName = row[0][3] + " " + row[0][4]
    now = datetime.now()
    formatted_now = now.strftime("%Y/%m/%d/%H/%M/%S")
    InsertSQL = ("INSERT INTO Message_Table(CustomerID, EmployeeID, FromName, ToName, MessageText, Product, Timestamp) VALUES(" + str(CustomerID) + ", " + str(EmployeeID) + ", '"+ str(EmployeeFullName) + "', '" + str(CustomerFullName) + "', '" + str(MessageText) + "', 'PS5', '" + str(formatted_now) + "')")
    print(InsertSQL)
    Insert_Data(database_file, InsertSQL)
    MessageThatCustomer()


########################################
#          Grab All Customers          #
########################################
def GetCustomers():
    global count
    if count == 0:
        count = count + 1
        query = ("SELECT * FROM Customer_Table")
        row = query_database(database_file, query)
        print(row)
        for i in range(0, len(row)):
            CustomerFirstName = row[i][3]
            CustomerSecondName = row[i][4]
            CustomerID = row[i][0]
            CustomerFullName = CustomerFirstName + " " + CustomerSecondName
            CustomerListbox.append(CustomerFullName)
    else:
        return

#############################
#          Graph 1          #
#############################
def Graph1():
    salesdata = pd.read_excel("Sales_csv.xlsx")
    plt.figure(figsize=(10,10))
    plt.bar(salesdata["Product"], salesdata["Profit"])
    plt.title('Tracking Groups Steps')
    plt.xlabel("Product")
    plt.ylabel("Profit")
    plt.xticks(rotation=90)
    plt.savefig(image_location1)
    plt.close()
    PictureGraph1.value = image_location1
    PictureGraph1.height = GraphSize
    PictureGraph1.width = GraphSize
#############################
#          Graph 2          #
#############################
def Graph2():
    salesdata = pd.read_excel("Sales_csv.xlsx")
    plt.figure(figsize=(10,10))
    salesdata["Date Bought"] = pd.to_datetime(salesdata["Date Bought"], format= "%d/%b/%Y")
    plt.plot(salesdata["Date Bought"], salesdata["Profit"])
    plt.title('Date Bought and Profit')
    plt.xlabel("Date")
    plt.ylabel("Profit")
    plt.xticks(rotation=90)
    plt.savefig(image_location2)
    plt.close()
    PictureGraph2.value = image_location2
    PictureGraph2.height = GraphSize
    PictureGraph2.width = GraphSize
#############################
#          Graph 3          #
#############################
def Graph3():
    salesdata = pd.read_excel("Sales_csv.xlsx")
    plt.figure(figsize=(10,10))
    plt.pie(salesdata["Amount sold"], labels=salesdata["Product"])
    plt.title('Pie Chart of Amount sold of products')
    plt.savefig(image_location3)
    plt.close()
    PictureGraph3.value = image_location3
    PictureGraph3.height = GraphSize
    PictureGraph3.width = GraphSize
#############################
#          Graph 4          #
#############################
def Graph4():
    salesdata = pd.read_excel("Sales_csv.xlsx")
    plt.figure(figsize=(10,10))
    plt.barh(salesdata["Product"], salesdata["Revenue"])
    plt.title('Product and its revenue')
    plt.xlabel("Revenue")
    plt.ylabel("Prroduct")
    plt.xticks(rotation=90)
    plt.savefig(image_location4)
    plt.close()
    PictureGraph4.value = image_location4
    PictureGraph4.height = GraphSize
    PictureGraph4.width = GraphSize
#####################################
#           Signout Button          #
#####################################
# signout button if the user wants to sign out of their account.
def SignOut():
    # emptys the textboxes on login and signup
    EmployeeUsernameTextbox.value = ""
    EmployeePasswordTextbox.value = ""
    CustomerUsernameTextbox.value = ""
    CustomerPasswordTextbox.value = ""
    CustomerSignUpUsernameTextbox.value = ""
    CustomerSignUpForenameTextbox.value = ""
    CustomerSignUpSurnameTextbox.value = ""
    CustomerSignUpEmailTextbox.value = ""
    CustomerSignUpDeliveryTextbox.value = ""
    CustomerSignUpPasswordTextbox.value = ""
    CustomerSignUpConfirmTextbox.value = ""
    # unchecks checkbox for terms and conditions
    CustomerTermsAndConditionsCheckbox.value = 0
    CustomerLoginSignUpPage.hide()
    CustomerLoginPage.hide()
    CustomerSignUpPage.hide()
    CustomerProductsPage.hide()
    CustomerMessagingPage.hide()
    EmployeeLoginPage.hide()
    EmployeeDashboardPage.hide()
    EmployeeProductsPage.hide()
    EmployeeCustomersPage.hide()
    EmployeeMessagingPage.hide()
    app.show()

def CustomerProductsNavigation():
    CustomerProductsPage.show()
    CustomerMessagingPage.hide()

def CustomerMessagesNavigation():
    CustomerMessagingPage.show()
    CustomerProductsPage.hide()
    CustomerViewMessages()

def EmployeeProductsNavigation():
    EmployeeProductsPage.show()
    EmployeeDashboardPage.hide()
    EmployeeCustomersPage.hide()
    EmployeeMessagingPage.hide()

def EmployeeDashboardNavigation():
    EmployeeProductsPage.hide()
    EmployeeDashboardPage.show()
    EmployeeCustomersPage.hide()
    EmployeeMessagingPage.hide()
    Graph1()
    Graph2()
    Graph3()
    Graph4()

def EmployeeCustomersNavigation():
    EmployeeProductsPage.hide()
    EmployeeDashboardPage.hide()
    EmployeeCustomersPage.show()
    EmployeeMessagingPage.hide()
    GetCustomers()

def EmployeeMessagingNavigation():
    EmployeeProductsPage.hide()
    EmployeeDashboardPage.hide()
    EmployeeCustomersPage.hide()
    EmployeeMessagingPage.show()
    

#################################
#           Light Mode          #
#################################
def LightMode():
    # lighter theme for users with eyesight that means they cant look at a dark screen.
    app.bg = "#F4F4F4"
    CustomerLoginSignUpPage.bg = "#F4F4F4"
    CustomerLoginPage.bg = "#F4F4F4"
    CustomerSignUpPage.bg = "#F4F4F4"
    CustomerProductsPage.bg = "#F4F4F4"
    CustomerMessagingPage.bg = "#F4F4F4"
    EmployeeLoginPage.bg = "#F4F4F4"
    EmployeeDashboardPage.bg = "#F4F4F4"
    EmployeeProductsPage.bg = "#F4F4F4"
    EmployeeCustomersPage.bg = "#F4F4F4"
    EmployeeMessagingPage.bg = "#F4F4F4"

################################
#           Dark Mode          #
################################
def DarkMode():
    # creates a dark theme for users with bad eyesight or too bright for them
    app.bg = "#808080"
    CustomerLoginSignUpPage.bg = "#808080"
    CustomerLoginPage.bg = "#808080"
    CustomerSignUpPage.bg = "#808080"
    CustomerProductsPage.bg = "#808080"
    CustomerMessagingPage.bg = "#808080"
    EmployeeLoginPage.bg = "#808080"
    EmployeeDashboardPage.bg = "#808080"
    EmployeeProductsPage.bg = "#808080"
    EmployeeCustomersPage.bg = "#808080"
    EmployeeMessagingPage.bg = "#808080"

######################
#     Navigation     #
######################
def CustomerButton():
    app.hide()
    CustomerLoginSignUpPage.show()

def EmployeeButton():
    app.hide()
    EmployeeLoginPage.show()

def dog():
    print("Dog")

def CustomerBackButton():
    CustomerLoginSignUpPage.hide()
    app.show()

def CustomerLoginPageNavigation():
    CustomerLoginPage.show()
    CustomerLoginSignUpPage.hide()

def CustomerSignUpPageNavigation():
    CustomerSignUpPage.show()
    CustomerLoginSignUpPage.hide()

def EmployeeLoginBackButton():
    app.show()
    EmployeeLoginPage.hide()

def CustomerLoginBackButton():
    CustomerLoginPage.hide()
    CustomerLoginSignUpPage.show()

def CustomerSignUpBackButton():
    CustomerSignUpPage.hide()
    CustomerLoginSignUpPage.show()

#############################################
#      Customer Create Account Button       #
#############################################

def CreateAccountButton():
    global CustomerID
    # validation on signing up
    if CustomerSignUpUsernameTextbox.value == "":
        info("Error!", "You must enter a Username!")
    elif len(CustomerSignUpUsernameTextbox.value) <= 3:
        info("Error!", "Username must be larger than 3 characters!")
    elif len(CustomerSignUpUsernameTextbox.value) >= 15:
        info("Error!", "Username too large must be below 15 characters!")
    elif CustomerSignUpForenameTextbox.value == "":
        info("Error!", "You must enter a Firstname!")
    elif CustomerSignUpSurnameTextbox.value == "":
        info("Error!", "You must enter a Surname!")
    elif CustomerSignUpEmailTextbox.value == "":
        info("Error!", "You must enter a Email!")
    elif "@" and "." not in CustomerSignUpEmailTextbox.value:
        info("Error!", "'Email' must have @ and a '.'!")
    elif CustomerSignUpDeliveryTextbox.value == "":
        info("Error!", "You must enter a Delivery Address!")
    elif CustomerSignUpPasswordTextbox.value == "":
        info("Error!", "You must enter a Password!")
    elif len(CustomerSignUpPasswordTextbox.value) <= 3:
        info("Error!", "Password must be larger than 3 characters!")
    elif len(CustomerSignUpPasswordTextbox.value) >= 12:
        info("Error!", "Password too large must be below 12 characters!")
    elif CustomerTermsAndConditionsCheckbox.value == 0:
        info("Error!", "In order to contine you have to accept the terms and conditions.")
    elif CustomerSignUpPasswordTextbox.value == CustomerSignUpConfirmTextbox.value:
        #insert the data into the database
        # encrypt the password.
        InsertSQL = ("INSERT INTO Customer_Table(Username, Password, Forename, Surname, Email, DeliveryAddress) VALUES('"+ str(CustomerSignUpUsernameTextbox.value) + "','" + str(CustomerSignUpPasswordTextbox.value) + "','" + str(CustomerSignUpForenameTextbox.value) + "','" + str(CustomerSignUpSurnameTextbox.value) + "','" + str(CustomerSignUpEmailTextbox.value) + "','" + str(CustomerSignUpDeliveryTextbox.value)+ "')")
        print(InsertSQL)
        Insert_Data(database_file, InsertSQL)
        CustomerSignUpPage.hide()
        CustomerProductsPage.show()
        query = ("SELECT * FROM Customer_Table WHERE Forename = '" + str(CustomerSignUpForenameTextbox.value) + "' AND Surname = '" + str(CustomerSignUpSurnameTextbox.value) + "'")
        print(query)
        row = query_database(database_file, query)
        CustomerID = row[0][0]
    else:
        # if password != to confirm password then it will output an error.
        info("Sorry!","You need to enter your in password the same time twice!")

####################################
#      Customer Login Button       #
####################################
def CustomerLoginButton():
    global CustomerID
    global CustomerFullName
    # validation for if null
    if CustomerUsernameTextbox.value =="":
        info("Error!", "You must enter a Username!")
    elif CustomerPasswordTextbox.value == "":
        info("Error!", "You must enter a Password!")
    else:
        # query to select all the usernames
        query = ("SELECT * from Customer_Table WHERE Username = "+ "'"+ str(CustomerUsernameTextbox.value) + "' AND Password = '" + str(CustomerPasswordTextbox.value) + "'")
        print(query)
        # gets that row 
        try:
            row = query_database(database_file, query)
        except sqlite3.Error:
            info("Error", "Dont do that again")
        if len(row) > 0:
            CustomerID = row[0][0]
            CustomerFullName = row[0][3] + " " + row[0][4]
            CustomerProductsPage.show()
            CustomerLoginPage.hide()
        else:
            info("Error!", "Your details are not in our database! Try again.")

####################################
#      Employee Login Button       #
####################################
def EmployeeLoginButton():
    global EmployeeID
    # validation for if null
    if EmployeeUsernameTextbox.value =="":
        info("Error!", "You must enter a Username!")
    elif EmployeePasswordTextbox.value == "":
        info("Error!", "You must enter a Password!")
    else:
        # query to select all the usernames
        query = ("SELECT * from Employee_Table WHERE Username = "+ "'"+ str(EmployeeUsernameTextbox.value) + "' AND Password = '" + str(EmployeePasswordTextbox.value) + "'")
        print(query)
        # gets that row 
        try:
            row = query_database(database_file, query)
        except sqlite3.Error:
            info("Error", "Dont do that again")
        if len(row) > 0:
            EmployeeID = row[0][0]
            EmployeeDashboardPage.show()
            Graph1()
            Graph2()
            Graph3()
            Graph4()
            EmployeeLoginPage.hide()
        else:
            info("Error!", "Your details are not in our database! Try again.")
#############################################
#                                           #
#              MAIN PROGRAMME               # 
#                                           #
#############################################
##########################################
#         Customer/Employee Page         #
##########################################
# creates the app / window
app = App(title = "Customer/Employee Page", layout="auto")
#
#app.after(1800000, SignOut)
# on all of these i am making it full screen for the user expeirence.
app.set_full_screen()
textblank = Text(app, text=" ")
textblank = Text(app, text=" ")
text = Text(app, text="Are you a Customer or Employee?", size=30)
textblank = Text(app, text=" ")
textblank = Text(app, text=" ")
box = Box(app, align="top", border = False, layout="grid")
# contains commands in the buttons so that when it is clicked a command function will happen this is event driven coding.
CustomerImage = Picture(box, image="Customer.png", grid=[0,0], width= 500, height=600)
textblank = Text(box, text="                ", grid=[1,0])
EmployeeImage = Picture(box, image="Employee.png", grid=[2,0], width= 500, height=600)
Customer_button = PushButton(box, text="Customer", grid = [0,2], command=CustomerButton, width = 20)
Customer_button.text_size = 25
textblank = Text(box, text=" ", grid = [0,1])
textblank = Text(box, text=" ", grid = [2,1])
Employee_button = PushButton(box, text="Employee", grid = [2,2], command=EmployeeButton, width = 20)
Employee_button.text_size = 25

###############################################
#         Customer Login/Sign-up Page         #
###############################################
CustomerLoginSignUpPage = Window(app, title="Customer Login/Sign-up Page")
CustomerLoginSignUpPage.set_full_screen()
CustomerLoginSignUpPage.hide()
textblank = Text(CustomerLoginSignUpPage, text=" ")
textblank = Text(CustomerLoginSignUpPage, text=" ")
text = Text(CustomerLoginSignUpPage, text="Please login, if you don't have a", size=30)
text = Text(CustomerLoginSignUpPage, text="account you can create one", size=30)
textblank = Text(CustomerLoginSignUpPage, text=" ")
textblank = Text(CustomerLoginSignUpPage, text=" ")
textblank = Text(CustomerLoginSignUpPage, text=" ")
textblank = Text(CustomerLoginSignUpPage, text=" ")
Customer_LoginPage_button = PushButton(CustomerLoginSignUpPage, text="Login", width = 15, command=CustomerLoginPageNavigation)
Customer_LoginPage_button.text_size = 25
textblank = Text(CustomerLoginSignUpPage, text=" ")
Customer_SignUpPage_button = PushButton(CustomerLoginSignUpPage, text="Sign-up", width = 15, command=CustomerSignUpPageNavigation)
Customer_SignUpPage_button.text_size = 25
textblank = Text(CustomerLoginSignUpPage, text=" ")
Customer_Back_button = PushButton(CustomerLoginSignUpPage, text="Back", width = 15, command=CustomerBackButton)
Customer_Back_button.text_size = 25
textblank = Text(CustomerLoginSignUpPage, text=" ")

#######################################
#         Customer Login Page         #
#######################################
CustomerLoginPage = Window(app, title="Customer Login Page")
CustomerLoginPage.hide()
CustomerLoginPage.set_full_screen()
textblank = Text(CustomerLoginPage, text=" ")
box2 = Box(CustomerLoginPage, width="fill", border = False)
# Widgets in box2
textblank = Text(box2, text=" ")
textblank = Text(box2, text=" ")
textblank = Text(box2, text=" ")
text = Text(box2, text="Enter your customer login:", width="fill", height= "fill", size=30)
textblank = Text(box2, text=" ")
textblank = Text(box2, text=" ")
textblank = Text(box2, text=" ")
textblank = Text(box2,  width="fill", height= "fill", text=" ")
textUsername = Text(box2, text="Username: ",  width="fill", height= "fill")
textUsername.text_size = 20
CustomerUsernameTextbox = TextBox(box2, hide_text=False,width=30, height= "fill")
CustomerUsernameTextbox.text_size = 20
textblank = Text(box2, text=" ")
textblank = Text(box2, text=" ")
textPassword = Text(box2, text="Password: ",   width="fill", height= "fill")
textPassword.text_size = 20
CustomerPasswordTextbox = TextBox(box2, hide_text=True, width=30, height= "fill")
CustomerPasswordTextbox.text_size = 20
textblank = Text(box2,  width="fill", height= "fill", text=" ")
# Buttons on Login Page
textblank = Text(CustomerLoginPage, text=" ")
Customer_Login_button = PushButton(CustomerLoginPage, text="Login", command=CustomerLoginButton, width=15)
Customer_Login_button.text_size = 25
textblank = Text(CustomerLoginPage, text=" ")
Customer_Login_Back_button = PushButton(CustomerLoginPage, text="Back", command=CustomerLoginBackButton, width=15)
Customer_Login_Back_button.text_size = 25

#########################################
#         Customer Sign-up Page         #
#########################################
CustomerSignUpPage = Window(app, title="Customer Sign-up Page")
CustomerSignUpPage.hide()
CustomerSignUpPage.set_full_screen()
textblank = Text(CustomerSignUpPage, text=" ")
textblank = Text(CustomerSignUpPage, text=" ")
textblank = Text(CustomerSignUpPage, text=" ")
text8 = Text(CustomerSignUpPage, text="Enter customer login details: ", size=30)
textblank = Text(CustomerSignUpPage, text=" ")
textblank = Text(CustomerSignUpPage, text=" ")
textblank = Text(CustomerSignUpPage, text=" ")
box3 = Box(CustomerSignUpPage, layout="grid")
# Widgets for Signup Page 
# Username text and textbox
textblank = Text(box3, text="               ", grid=[1,0])
text1 = Text(box3, text="Username:", align = "left", grid=[0,0])
text1.text_size = 20
CustomerSignUpUsernameTextbox = TextBox(box3, hide_text=False, align="left", grid=[2,0], width=20)
CustomerSignUpUsernameTextbox.text_size = 20
# Forename text and textbox
textblank = Text(box3, text="                       ", grid=[1,1])
text2 = Text(box3, text="Forename:", align = "left", grid=[0,1])
text2.text_size = 20
CustomerSignUpForenameTextbox = TextBox(box3, hide_text=False, width=20, height= "fill", grid=[2,1])
CustomerSignUpForenameTextbox.text_size = 20
# Surname text and textbox
textblank = Text(box3, text="                       ", grid=[1,2])
text3 = Text(box3, text="Surname: ",   align = "left", grid=[0,2])
text3.text_size = 20
CustomerSignUpSurnameTextbox = TextBox(box3, hide_text=False, width=20, height= "fill", grid=[2,2])
CustomerSignUpSurnameTextbox.text_size = 20
# Email text and textbox
textblank = Text(box3, text="                       ", grid=[1,3])
text4 = Text(box3, text="Email: ",    align = "left", grid=[0,3])
text4.text_size = 20
CustomerSignUpEmailTextbox = TextBox(box3, hide_text=False, width=20, height= "fill",grid=[2,3])
CustomerSignUpEmailTextbox.text_size = 20
# Date of Birth text and textbox
textblank = Text(box3, text="                       ", grid=[1,4])
text5 = Text(box3, text="Delivery Address: ",   align = "left", grid=[0,4])
text5.text_size = 20
CustomerSignUpDeliveryTextbox = TextBox(box3, hide_text=False, width=20, height= "fill",grid=[2,4])
CustomerSignUpDeliveryTextbox.text_size = 20
# Password text and textbox
textblank = Text(box3, text="                       ", grid=[1,5])
text6 = Text(box3, text="Password: ",    align = "left", grid=[0,5])
text6.text_size = 20
CustomerSignUpPasswordTextbox = TextBox(box3, hide_text=True, width=20, height= "fill",grid=[2,5])
CustomerSignUpPasswordTextbox.text_size = 20
# Confirm Password text and textbox
textblank = Text(box3, text="                       ", grid=[1,6])
text7 = Text(box3, text="Confirm Password: ",    align = "left", grid=[0,6])
text7.text_size = 20
CustomerSignUpConfirmTextbox = TextBox(box3, hide_text=True, width=20, height= "fill",grid=[2,6])
CustomerSignUpConfirmTextbox.text_size = 20
# Accept Terms and Conditions
textblank = Text(CustomerSignUpPage, text="                       ")
CustomerTermsAndConditionsCheckbox = CheckBox(CustomerSignUpPage, text=" Please Accept the Terms and Conditions if you wish to continue")
CustomerTermsAndConditionsCheckbox.text_size = 15
# Buttons for Signup Page
textblank = Text(CustomerSignUpPage, text="                       ")
Customer_SignUp_button = PushButton(CustomerSignUpPage, text="Create Account", command=CreateAccountButton, width=15)
Customer_SignUp_button.text_size = 25
textblank = Text(CustomerSignUpPage, text=" ")
Customer_SignUp_Back_button = PushButton(CustomerSignUpPage, text="Back", command=CustomerSignUpBackButton, width=15)
Customer_SignUp_Back_button.text_size = 25
##########################################
#         Customer Products Page         #
##########################################
CustomerProductsPage = Window(app, title="Customer Products Page")
CustomerProductsPage.hide()
CustomerProductsPage.set_full_screen()
textblank = Text(CustomerProductsPage, text= " ")
GameStarzText = Picture(CustomerProductsPage, image="GameStarzText.png", width=500 , height=100)
# creates a box to put all the navigation buttons in.
NavigationBar = Box(CustomerProductsPage, layout = "grid", border=True)
# buttons
ProductsPagebutton = PushButton(NavigationBar, text="Products",  grid=[0,0], width=51, command=CustomerProductsNavigation)
MessagesPagebutton = PushButton(NavigationBar, text="Messages", grid=[1,0], width=51, command=CustomerMessagesNavigation)
DarkModeButton = PushButton(NavigationBar, text="Dark Mode", grid=[2,0], width=51, command=DarkMode)
LightModeButton = PushButton(NavigationBar, text="Light Mode", grid=[3,0], width=51, command=LightMode)
SignOut_Button = PushButton(NavigationBar, text="Sign out", grid=[4,0], width=51, command=SignOut)
ProductsBox = Box(CustomerProductsPage, layout = "grid", border=False)
Product1 = Picture(ProductsBox, image="PS5.png", grid= [0,0], width = 600, height= 400)
Product2 = Picture(ProductsBox, image= "PS4Slim.png", grid= [1,0], width = 600, height= 400)
Product3 = Picture(ProductsBox, image= "PS4Pro.png", grid= [2,0], width = 600, height= 400)
ProductText1 = Text(ProductsBox, text= "PS5 - £450.00", grid= [0,1], size = 20)
ProductText2 = Text(ProductsBox, text= "PS4 Slim - £260.00", grid= [1,1], size = 20)
ProductText3 = Text(ProductsBox, text= "PS4 Pro - £295.00", grid= [2,1], size = 20)
Product4 = Picture(ProductsBox, image= "NintendoSwitch.png", grid= [0,2], width = 600, height= 400)
Product5 = Picture(ProductsBox, image= "XboxSeriesX.png", grid= [1,2], width = 600, height= 400)
Product6 = Picture(ProductsBox, image= "XboxOneS.png", grid= [2,2], width = 600, height= 400)
ProductText4 = Text(ProductsBox, text= "Nintendo Switch = £340.00", grid= [0,3], size = 20)
ProductText5 = Text(ProductsBox, text= "Xbox Series X - £450.00", grid= [1,3], size = 20)
ProductText6 = Text(ProductsBox, text= "Xbox One S - £200.00", grid= [2,3], size = 20)
# creates info for user to see and read.
# uses boxes to split up the page.
##########################################
#         Customer Messages Page         #
##########################################
CustomerMessagingPage = Window(app, title="Customer Messages Page")
CustomerMessagingPage.hide()
CustomerMessagingPage.set_full_screen()
textblank = Text(CustomerMessagingPage, text= " ")
GameStarzText = Picture(CustomerMessagingPage, image="GameStarzText.png", width=500 , height=100)
# creates a box to put all the navigation buttons in.
NavigationBar2 = Box(CustomerMessagingPage, layout = "grid", border=True)
# buttons
ProductsPagebutton = PushButton(NavigationBar2, text="Products",  grid=[0,0], width=51, command=CustomerProductsNavigation)
MessagesPagebutton = PushButton(NavigationBar2, text="Messages", grid=[1,0], width=51, command=CustomerMessagesNavigation)
DarkModeButton = PushButton(NavigationBar2, text="Dark Mode", grid=[2,0], width=51, command=DarkMode)
LightModeButton = PushButton(NavigationBar2, text="Light Mode", grid=[3,0], width=51, command=LightMode)
SignOut_Button = PushButton(NavigationBar2, text="Sign out", grid=[4,0], width=51, command=SignOut)

Message_Grid = Box(CustomerMessagingPage, layout = "grid", border = True)
textblank = Text(Message_Grid, text = "                                          ", grid = [0,0], size = 20)
textblank = Text(Message_Grid, text = "                                                                     ", grid = [1,0], size = 20)
CEmployeeMessage1 = Text(Message_Grid, text = "                                          ", grid = [2,0], size = 20)
CCustomerMessage1 = Text(Message_Grid, text = "                                          ", grid = [0,1], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,1], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [2,1], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [0,2], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,2], size = 20)
CEmployeeMessage2 = Text(Message_Grid, text = "                                          ", grid = [2,2], size = 20)
CCustomerMessage2 = Text(Message_Grid, text = "                                          ", grid = [0,3], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,3], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [2,3], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [0,4], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,4], size = 20)
CEmployeeMessage3 = Text(Message_Grid, text = "                                            ", grid = [2,4], size = 20)
TextAndSendBox = Box(CustomerMessagingPage, layout = "grid", border = True)
CustomerMessageTextbox = TextBox(TextAndSendBox, grid = [0,0], width = 60)
CustomerMessageTextbox.text_size = 20
SendMessage_Button = PushButton(TextAndSendBox, text = "Send", grid = [1,0], width = 20, command=CustomerSendMessage)
SendMessage_Button.text_size = 20
textblank = Text(CustomerMessagingPage, text= " ")
Refresh_Button = PushButton(CustomerMessagingPage, text = "Refresh Messages", width = 20, command=CustomerViewMessages)
Refresh_Button.text_size = 20
#######################################
#         Employee Login Page         #
#######################################
EmployeeLoginPage = Window(app, title="Employee Login Page")
EmployeeLoginPage.hide()
EmployeeLoginPage.set_full_screen()
# Create Login Page
textblank = Text(EmployeeLoginPage, text=" ")
box4 = Box(EmployeeLoginPage, width="fill")
# Widgets in box3
textblank = Text(box4, text=" ")
textblank = Text(box4, text=" ")
textblank = Text(box4, text=" ")
text = Text(box4, text="Enter your employee login:", width="fill", height= "fill", size=30)
textblank = Text(box4, text=" ")
textblank = Text(box4, text=" ")
textblank = Text(box4, text=" ")
textblank = Text(box4,  width="fill", height= "fill", text=" ")
TextUsername1 = Text(box4, text="Username: ",  width="fill", height= "fill")
TextUsername1.text_size = 20
EmployeeUsernameTextbox = TextBox(box4, hide_text=False,width=30, height= "fill")
EmployeeUsernameTextbox.text_size = 20
textblank = Text(box4, text=" ")
textblank = Text(box4, text=" ")
TextPassword1 = Text(box4, text="Password: ",   width="fill", height= "fill")
TextPassword1.text_size = 20
EmployeePasswordTextbox = TextBox(box4, hide_text=True, width=30, height= "fill")
EmployeePasswordTextbox.text_size = 20
textblank = Text(box4,  width="fill", height= "fill", text=" ")
# Buttons on Login Page
textblank = Text(EmployeeLoginPage, text=" ")
Employee_Login_button = PushButton(EmployeeLoginPage, text="Login", command=EmployeeLoginButton, width=15)
Employee_Login_button.text_size = 25
textblank = Text(EmployeeLoginPage, text=" ")
Employee_Back_button = PushButton(EmployeeLoginPage, text="Back", command=EmployeeLoginBackButton, width=15)
Employee_Back_button.text_size = 25

###########################################
#         Employee Dashboard Page         #
###########################################
EmployeeDashboardPage = Window(app, title="Employee Dashboard Page")
EmployeeDashboardPage.hide()
EmployeeDashboardPage.set_full_screen()

textblank = Text(EmployeeDashboardPage, text= " ")
GameStarzText = Picture(EmployeeDashboardPage, image="GameStarzText.png", width=500 , height=100)
# creates a box to put all the navigation buttons in.
NavigationBar3 = Box(EmployeeDashboardPage, layout = "grid", border=True)
# buttons
DashboardPagebutton = PushButton(NavigationBar3, text="Dashboard",  grid=[0,0], width=42, command=EmployeeDashboardNavigation)
CustomersPagebutton = PushButton(NavigationBar3, text="Customers", grid=[1,0], width=42, command=EmployeeCustomersNavigation)
Productsbutton = PushButton(NavigationBar3, text="Products", grid=[2,0], width=42, command=EmployeeProductsNavigation)
DarkModeButton = PushButton(NavigationBar3, text="Dark Mode", grid=[3,0], width=42, command=DarkMode)
LightModeButton = PushButton(NavigationBar3, text="Light Mode", grid=[4,0], width=42, command=LightMode)
SignOut_Button = PushButton(NavigationBar3, text="Sign out", grid=[5,0], width=42, command=SignOut)

GraphsBox = Box(EmployeeDashboardPage, layout = "grid", border=True)
PictureGraph1 = Picture(GraphsBox, grid = [0,0])
textblank = Text(GraphsBox, text= "                                              ", grid=[1,0])
PictureGraph2 = Picture(GraphsBox, grid = [2,0])
PictureGraph3 = Picture(GraphsBox, grid = [0,1])
textblank = Text(GraphsBox, text= "                                              ", grid=[1,1])
PictureGraph4 = Picture(GraphsBox, grid = [2,1])
###########################################
#         Employee Products Page         #
###########################################
EmployeeProductsPage = Window(app, title="Employee Products Page")
EmployeeProductsPage.hide()
EmployeeProductsPage.set_full_screen()

textblank = Text(EmployeeProductsPage, text= " ")
GameStarzText = Picture(EmployeeProductsPage, image="GameStarzText.png", width=500 , height=100)
# creates a box to put all the navigation buttons in.
NavigationBar3 = Box(EmployeeProductsPage, layout = "grid", border=True)
# buttons
DashboardPagebutton = PushButton(NavigationBar3, text="Dashboard",  grid=[0,0], width=42, command=EmployeeDashboardNavigation)
CustomersPagebutton = PushButton(NavigationBar3, text="Customers", grid=[1,0], width=42, command=EmployeeCustomersNavigation)
Productsbutton = PushButton(NavigationBar3, text="Products", grid=[2,0], width=42, command=EmployeeProductsNavigation)
DarkModeButton = PushButton(NavigationBar3, text="Dark Mode", grid=[3,0], width=42, command=DarkMode)
LightModeButton = PushButton(NavigationBar3, text="Light Mode", grid=[4,0], width=42, command=LightMode)
SignOut_Button = PushButton(NavigationBar3, text="Sign out", grid=[5,0], width=42, command=SignOut)
ProductsBox = Box(EmployeeProductsPage, layout = "grid", border=False)
Product1 = Picture(ProductsBox, image="PS5.png", grid= [0,0], width = 600, height= 400)
Product2 = Picture(ProductsBox, image= "PS4Slim.png", grid= [1,0], width = 600, height= 400)
Product3 = Picture(ProductsBox, image= "PS4Pro.png", grid= [2,0], width = 600, height= 400)
ProductText1 = Text(ProductsBox, text= "PS5 - £450.00", grid= [0,1], size = 20)
ProductText2 = Text(ProductsBox, text= "PS4 Slim - £260.00", grid= [1,1], size = 20)
ProductText3 = Text(ProductsBox, text= "PS4 Pro - £295.00", grid= [2,1], size = 20)
Product4 = Picture(ProductsBox, image= "NintendoSwitch.png", grid= [0,2], width = 600, height= 400)
Product5 = Picture(ProductsBox, image= "XboxSeriesX.png", grid= [1,2], width = 600, height= 400)
Product6 = Picture(ProductsBox, image= "XboxOneS.png", grid= [2,2], width = 600, height= 400)
ProductText4 = Text(ProductsBox, text= "Nintendo Switch = £340.00", grid= [0,3], size = 20)
ProductText5 = Text(ProductsBox, text= "Xbox Series X - £450.00", grid= [1,3], size = 20)
ProductText6 = Text(ProductsBox, text= "Xbox One S - £200.00", grid= [2,3], size = 20)
###########################################
#         Employee Customers Page         #
###########################################
EmployeeCustomersPage = Window(app, title="Employee Customers Page")
EmployeeCustomersPage.hide()
EmployeeCustomersPage.set_full_screen()

GameStarzText = Picture(EmployeeCustomersPage, image="GameStarzText.png", width=500 , height=100)
textblank = Text(EmployeeCustomersPage, text= " ")
# creates a box to put all the navigation buttons in.
NavigationBar3 = Box(EmployeeCustomersPage, layout = "grid", border=True)
# buttons
DashboardPagebutton = PushButton(NavigationBar3, text="Dashboard",  grid=[0,0], width=42, command=EmployeeDashboardNavigation)
CustomersPagebutton = PushButton(NavigationBar3, text="Customers", grid=[1,0], width=42, command=EmployeeCustomersNavigation)
Productsbutton = PushButton(NavigationBar3, text="Products", grid=[2,0], width=42, command=EmployeeProductsNavigation)
DarkModeButton = PushButton(NavigationBar3, text="Dark Mode", grid=[3,0], width=42, command=DarkMode)
LightModeButton = PushButton(NavigationBar3, text="Light Mode", grid=[4,0], width=42, command=LightMode)
SignOut_Button = PushButton(NavigationBar3, text="Sign out", grid=[5,0], width=42, command=SignOut)


CustomerListbox = ListBox(EmployeeCustomersPage, items=[])
Message_Customer_Button = PushButton(EmployeeCustomersPage, text="Message Customer", command=MessageThatCustomer)
###########################################
#         Employee Messaging Page         #
###########################################
EmployeeMessagingPage = Window(app, title="Employee Messaging Page")
EmployeeMessagingPage.hide()
EmployeeMessagingPage.set_full_screen()

GameStarzText = Picture(EmployeeMessagingPage, image="GameStarzText.png", width=500 , height=100)
textblank = Text(EmployeeMessagingPage, text= " ")
# creates a box to put all the navigation buttons in.
NavigationBar3 = Box(EmployeeMessagingPage, layout = "grid", border=True)
# buttons
DashboardPagebutton = PushButton(NavigationBar3, text="Dashboard",  grid=[0,0], width=42, command=EmployeeDashboardNavigation)
CustomersPagebutton = PushButton(NavigationBar3, text="Customers", grid=[1,0], width=42, command=EmployeeCustomersNavigation)
Productsbutton = PushButton(NavigationBar3, text="Products", grid=[2,0], width=42, command=EmployeeProductsNavigation)
DarkModeButton = PushButton(NavigationBar3, text="Dark Mode", grid=[3,0], width=42, command=DarkMode)
LightModeButton = PushButton(NavigationBar3, text="Light Mode", grid=[4,0], width=42, command=LightMode)
SignOut_Button = PushButton(NavigationBar3, text="Sign out", grid=[5,0], width=42, command=SignOut)
textblank = Text(EmployeeMessagingPage, text= " ")
Message_Grid = Box(EmployeeMessagingPage, layout = "grid", border = True)
textblank = Text(Message_Grid, text = "                                          ", grid = [0,0], size = 20)
textblank = Text(Message_Grid, text = "                                                                     ", grid = [1,0], size = 20)
EmployeeMessage1 = Text(Message_Grid, text = "                                          ", grid = [2,0], size = 20)
CustomerMessage1 = Text(Message_Grid, text = "                                          ", grid = [0,1], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,1], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [2,1], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [0,2], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,2], size = 20)
EmployeeMessage2 = Text(Message_Grid, text = "                                          ", grid = [2,2], size = 20)
CustomerMessage2 = Text(Message_Grid, text = "                                          ", grid = [0,3], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,3], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [2,3], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [0,4], size = 20)
textblank = Text(Message_Grid, text = "                                          ", grid = [1,4], size = 20)
EmployeeMessage3 = Text(Message_Grid, text = "                                            ", grid = [2,4], size = 20)
TextAndSendBox = Box(EmployeeMessagingPage, layout = "grid", border = True)
MessageTextbox = TextBox(TextAndSendBox, grid = [0,0], width = 60)
MessageTextbox.text_size = 20
SendMessage_Button = PushButton(TextAndSendBox, text = "Send", grid = [1,0], width = 20, command=EmployeeSendMessage)
SendMessage_Button.text_size = 20
textblank = Text(EmployeeMessagingPage, text= " ")
Refresh_Button = PushButton(EmployeeMessagingPage, text = "Refresh Messages", width = 20, command=dog)
Refresh_Button.text_size = 20
########################################
#         Calling the Database         #
########################################
# this bit of code called the functions that delete the existing database named FitnessApp, and then create a brand new one using DDL and DML sql in files and by calling these functions
delete_database(database_file)
init_db(database_file, "CreateDatabase.sql")
init_db(database_file, "DummyData.sql")
###############################
#         Display app         #
###############################
app.display()
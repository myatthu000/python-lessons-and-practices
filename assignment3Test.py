# Assignment 2
# reading, loading, recording data from/to file


from ast import literal_eval
from time import sleep

db={}
global counter
counter: int = 0
file_name = "2-assignment-test.txt"


global email_exit
email_exit=-1

def main_sector():
    print("Welcome from Form")
    main_option =str(input("Press 1 to Register:\nPress 2 to Login\nPress 3 Exit:"))
    if main_option== '1':
        registration()
    elif main_option=='2':
        login()
    elif main_option=='3':
        print("....................... Bye Bye .....................\n")
        sleep(1)
        exit(1)
    else:
        print("Invalid Option")
        main_sector()

def registration():
    print("\nRegister Your Account")
    global counter, db
    user_email = input("Enter your email:")
    email_get = Email_exit(user_email)

    if email_get!=None:
        print("Email already exit:")
        registration()
    else:
        user_name = input("Enter your username:")
        user_password = input("Enter your password:")
        user_phone = int(input("Enter your phone:"))
        user_age = int(input("Enter your age:"))
        # id = len(db)
        id = counter
        # to_insert = {counter: {'user': user_name, 'email': user_email, 'password': user_password, 'phone': user_phone, 'age': user_age}}
        to_insert = {id: {"u_name": user_name, "email": user_email, "password": user_password, "phone": user_phone, "age": user_age}}
        db.update(to_insert)
        print("\n")
        print("Register Successfully: ")
        # printing_all_data()
        printing_single_data(db,id)
        print("\n")
        recording_all_data(str(db))
        counter = len(db)
        # print ('db',db)


def login():
    print("\nLogin Your Account")

    user_found=-1;
    print("This is login sector")
    l_user_email = input("Enter your email to login:")
    l_user_password = input("Enter your password to login:")


    for i in range(len(db)):
        if db[i]["email"] == l_user_email and db[i]["password"]==l_user_password:

            user_found=i
    if user_found!=-1:
        print("Login Success!")
        user_profile(user_found)
    else:
        print("Not Found ")

def user_profile(user_found):
    print("\nWelcome:",db[user_found]["u_name"])
    printing_all_data()
    user_options = str(input("\nPress [1] to Update User Information \nPress [2] to Logout \n"))
# while(user_options):
    if user_options == '1':
        edit_user_info(user_found)
        # break
    elif user_options == '2':
        print("\nLogin user {0} is logout \n".format(db[user_found]["u_name"]))
        # recording_all_data(str(db))
        # break
    else:
        print("Invalid Option:\n")
        user_profile(user_found)
        # break
    # break

def edit_user_info(user_found):
    print("\n\nUser Information Edit Section : ")
    # edit_email is used for edit
    edit_email = str(input("Enter User Email to Edit Info : \nOr Type [cancel] to Cancel edition : "))
    datas = db
    email_id = Email_exit(edit_email)
    if edit_email != "cancel":
        if email_id !=None:
            printing_single_data(datas,email_id)
            print("\nEdit Account Section :")
            user_edit_data_choice_section(datas,email_id,user_found)
        else:
            print("\n{0} email does not exit in database : ".format(edit_email))
    else:
        sleep(2)
        print("going back to user profile .....")
        user_profile(user_found)


def Email_exit(email):

    lenght = len(db)
    for i in range(lenght):
        if db[i]["email"] == email:

            return i

def user_edit_data_choice_section(datas,email_id,user_found):
# while(email_id !=None):
    edit_email_option = str(input("Enter [1] to edit email: \nEnter [2] to edit username: \nEnter [3] to edit password: \nEnter [4] to edit age: \nEnter [5] to edit phone: \nEnter [6] to exit :\n"))
    if edit_email_option == '1':
        print("Edit Email: \n")
        edit_email_data = str(input("Edit email:... "))
        datas[email_id]['email'] = edit_email_data
        printing_single_data(datas,email_id)
        # record in txt file left
        print("\nSuccessfully updated email:... \n")
        recording_all_data(db)
        # print(db)

    elif edit_email_option == '2':
        print("Edit Username: \n")
        edit_username_data = str(input("Edit Username :... "))
        datas[email_id]['u_name'] = edit_username_data
        printing_single_data(datas, email_id)
        # record in txt file left
        print("\nSuccessfully updated username:... \n")
        recording_all_data(db)

    elif edit_email_option == '3':
        print("Edit Password: \n")
        edit_password_data = str(input("Edit password:... "))
        datas[email_id]['password'] = edit_password_data
        printing_single_data(datas, email_id)
        # record in txt file left
        print("\nSuccessfully updated password:... \n")
        recording_all_data(db)

    elif edit_email_option == '4':
        print("Edit Age: \n")
        edit_age_data = str(input("Edit Age:... "))
        datas[email_id]['age'] = edit_age_data
        printing_single_data(datas, email_id)
        # record in txt file left
        print("\nSuccessfully updated age:... \n")
        recording_all_data(db)


    elif edit_email_option == '5':
        print("Edit Phone: \n")
        edit_age_data = str(input("Edit Phone:... "))
        datas[email_id]['phone'] = edit_age_data
        printing_single_data(datas, email_id)
        # record in txt file left
        print("\nSuccessfully updated phone:... \n")
        recording_all_data(db)

    elif edit_email_option == '6':
        print("exit: \n")
        user_profile(user_found)
        recording_all_data(db)

    else:
        print("Invalid Option \n")
        user_edit_data_choice_section(datas,email_id,user_found)
        # break
    user_profile(user_found)

def create_txt_file_if_not_exit():
    try:
        with open(file_name, 'x') as createFile:
            createFile.close()
            print("File created successfully \n")
    except FileExistsError:
        print("File already created")

# data = {3:{'u_name': 'myat', 'email': 'myat@gmail.com', 'password': 'password', 'phone': 92222, 'age': 23}}
# db.update(data)

def recording_all_data(datas):
    # pass
    global db
    # db.update(data)
    with open(file_name, 'w') as writeFile:
        write = writeFile.write("{0}".format(str(datas)))


def printing_all_data():
    if db != {}:
        datas = db
        # print('db \n', db)
        counter = len(db)
        total = counter
        # print('counter \n', counter)
        print("Total User Accounts : {0}".format(total))
        print("..................................\n")
        for i in range(len(datas)):
            print("user_id: {0} \nusername: {1} \nemail: {2} \npassword: {3} \nphone_number: {4} \nage: {5}\n".format(i,datas[i]['u_name'],datas[i]['email'],datas[i]['password'],datas[i]['phone'],datas[i]['age']))
        print("..................................\n")

def printing_single_data(datas,i):
    print("\nuser_id: {0} \nusername: {1} \nemail: {2} \npassword: {3} \nphone_number: {4} \nage: {5} \n".format(i,datas[i]['u_name'], datas[i]['email'], datas[i]['password'], datas[i]['phone'], datas[i]['age']))

def loading_all_data():
    global db, counter
    with open(file_name, 'r') as readFile:
        read = readFile.read()
        # print("dsdasdf ", read=='')
        if read != '':
            read = literal_eval(read)
            db = read
            counter = len(db)
        else:
            print("Data is Empty \n")
        # print('type = {0} \n data = {1} \n length = {2}'.format(type(read), read,len(db)))
        # db = read
        # print('type = {0} \n data = {1} '.format(type(db), db))


if __name__ == '__main__':
   create_txt_file_if_not_exit()
   loading_all_data()
   printing_all_data()
   # recording_all_data()
   while True:
       main_sector()
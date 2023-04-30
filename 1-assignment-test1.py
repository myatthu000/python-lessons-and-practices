# Assignment 1 file IO
# Loading all data from file
# printing all data from file
# Record user data in txt file

db={}
global id
id = 0

global email_exit
email_exit=-1

def main_sector():
    main_option =int(input("Press 1 to Register:\nPress 2 to Login\nPress 3 Exit:"))
    if main_option== 1:
        registration()
    elif main_option==2:
        login()
    elif main_option==3:
        exit(1)
    else:
        print("Invalid Option")
        main_sector()


def registration():
    id = loading_all_data()[0]
    # print('id', id)
    global db1
    db = loading_all_data()[1]
    # print('db = ',db)

    user_email = input("Enter your email:")
    email_get = Email_exit(user_email)


    if email_get!=None:
        print("Email already exit:")
        registration()
    else:
        counter = loading_all_data()[0]
        print('id', counter)
        user_name = input("Enter your username:")
        user_password = input("Enter your password:")
        user_phone = int(input("Enter your phone:"))
        user_age = int(input("Enter your age:"))

        to_insert = {counter: {'user': user_name, 'email': user_email, 'password': user_password, 'phone': user_phone, 'age': user_age}}
        # to_insert = {counter: {"email": user_email,"u_name":user_name, "password": user_password,"phone":user_phone,"age":user_age}}
        db.update(to_insert)
        recording_all_data(str(db))


def login():
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
    print("Welcome:",db[user_found]["u_name"])

    option =int(input("Press 1 to exit"))
    if option == 1:
        recording_all_data()


def Email_exit(email):

    lenght = len(db)
    for i in range(lenght):
        if db[i]["email"] == email:

            return i


def recording_all_data(data):
    with open("1_assignment.txt",'w') as writeFile:
        writeFile.write(data)
        writeFile.write('\n')
    writeFile.close()

# from file to dict

def create_txt_file():
    try:
        with open('3_assignment.txt', 'x') as createFile:
            createFile.close()
    except FileExistsError:
        print("Text file already exit \n")


def loading_all_data():
    # pass
    global id, db
    try:
        with open('3_assignment.txt', 'r') as readFile:
            datas = readFile.read()
            data_dist_from_str = eval(datas)
            # print('---->', data_dist_from_str)
            db = data_dist_from_str
            id = len(db)
            readFile.close()
    except FileNotFoundError:
        print("File not found \n")
        if FileNotFoundError:
            create_txt_file()
            print("Text file is created \n")
    # finally:
    #     pass
        # readFile.close()

    # with open('3_assignment.txt', 'r') as readFile:
    #     datas = readFile.read()
    #     data_dist_from_str = eval(datas)
    #     db = data_dist_from_str
    #     id = len(db)

    # id = len(db)
    return [id,db]


def printing_all_data():
    datas = loading_all_data()[1]
    # print('datas ---> ',datas)
    for i in range(len(datas)):
        print("user_id: {0} username: {1} email: {2} password: {3} phone_number: {4} age: {5}".format(i,
                                                                                                 datas[i][
                                                                                                     'user'],
                                                                                                 datas[i][
                                                                                                     'email'],
                                                                                                 datas[i][
                                                                                                     'password'],
                                                                                                 datas[i][
                                                                                                     'phone'],
                                                                                                 datas[i][
                                                                                                     'age']))



if __name__ == '__main__':
    # print(loading_all_data()[1])
    printing_all_data()
    # print(loading_all_data()[0])
    # print(id)
    while True:
        main_sector()
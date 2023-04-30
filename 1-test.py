from ast import literal_eval

db={}
global counter
counter: int = 0


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
        printing_all_data()
        recording_all_data(str(db))
        counter = len(db)


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


def create_txt_file_if_not_exit():
    try:
        with open("1-test.txt", 'x') as createFile:
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
    with open("1-test.txt", 'a') as writeFile:
        write = writeFile.write("{0}".format(str(datas)))


def printing_all_data():
    # if db
    print('db \n', db == )
    counter = len(db)
    # print('counter \n', counter)


def loading_all_data():
    global db, counter
    with open("1-test.txt", 'r') as readFile:
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
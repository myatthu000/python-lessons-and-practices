global db2, data_base, counter
data_base : dict = {}
db2 : dict = {}
counter: int = 0


distt = {
        0: {'user': 'winwin', 'email': 'win@gmail.com', 'password': 'password', 'phone': 12345, 'age': 23},
        1: {'user': 'myatmyat', 'email': 'myat@gmail.com', 'password': 'password', 'phone': 3232323, 'age': 20},
        2: {'user': 'uu', 'email': 'uu@gmail.com', 'password': 'password', 'phone': 91212121, 'age': 23},
        3: {'user': 'yy', 'email': 'yy@gmail.com', 'password': 'password', 'phone': 91212121, 'age': 23}
    }


# print('distt before',distt)
# print(distt[3])


datas = {4: {'user': 'emo', 'email': 'emo@gmail.com', 'password': 'password', 'phone': 91212121, 'age': 23}}
distt.update(datas)
print(distt[4])

def register():
    global id
    id = counter
    print('id',id)
    user_name = str(input("enter name:"))
    email = str(input("enter email:"))
    password = str(input("enter password:"))
    phone_no = int(input("enter phone:"))
    age = int(input("enter age:"))
    distt.update({id: {'user': user_name, 'email': email, 'password': password, 'phone': phone_no, 'age': age}})
    print('updated-->',distt[id])
    print('updated',distt)

# print('distt after',distt)

# key = datas.keys()
# value = datas.values()
# print(key,value)

def reading_all_data_from_file():
    global db2, counter
    with open("2_assignment.txt",'r') as readFile:
        datas = readFile.read()
        # print(datas[-2])
        db2 = eval(datas)
        counter = len(db2)
    readFile.close()


def printing_data():
    global db2, counter
    print('counter',counter)
    # datas = db2
    for i in range(len(db2)):
        # print("username : {0}".format(data_base[i]['user']))
        print("user_id: {0} username: {1} email: {2} password: {3} phone_number: {4} age: {5}".format(i,
                                                                                                      db2[i][
                                                                                                          'user'],
                                                                                                      db2[i][
                                                                                                          'email'],
                                                                                                      db2[i][
                                                                                                          'password'],
                                                                                                      db2[i][
                                                                                                          'phone'],
                                                                                                      db2[i][
                                                                                                          'age']))


def recording_all_data_to_file(data):
    with open("2_assignment.txt",'w') as writeFile:
        # writeFile.write(',\n')
        # for line in data:
        #     writeFile.writelines(line)
        writeFile.write(data)
    writeFile.close()



if __name__ == '__main__':
    printing_data()
    reading_all_data_from_file()
    # register()
    recording_all_data_to_file(str(distt))
    printing_data()
    # for i in db2:
    #     print(db2[i]['age'])


# data = str(input('Enter some text ...'))

# with open('test2.txt','a') as file:
#     file.write(data)
#     file.write('\n')



id = 0

distt = {
        0: {'user': 'winwin', 'email': 'win@gmail.com', 'password': 'password','phone':12345 , 'age': 23},
        1: {'user': 'myatmyat', 'email': 'myat@gmail.com', 'password': 'password','phone':3232323 , 'age': 20},
        2: {'email': 'uu@gmail.com', 'u_name': 'uu', 'password': 'password', 'phone': 12, 'age': 23},
        3: {'email': 'yy@gmail.com', 'u_name': 'yy', 'password': 'password', 'phone': 91212121, 'age': 23}
    }



length = len(distt)
print('len',length)

# for j in range(len(distt)):
#     for i in range(len(distt[j])):
#         # print('user data in distt: ',(distt[j][i]))
#         pass

# print(len(distt[0]),len(distt))
# print('000',distt[0][1])
# print('ddd',distt[0])

# data = str(input('Enter'))
#
# with open('1_assignment.txt','a') as file:
#     read_data = file.readlines()
#     for i in range(len(read_data)):
#         pass
#         # print(read_data[i][0]['user'])
#         # print('id:{0}'.format(read_data[i]))
#     # print(read_data)
#
# file.close()

data_base: dict = {}

# with open("1_assignment.txt",'r') as readFile:
#     datas = readFile.read()
    # print(type(datas))
    # data_base[] = datas
    # data_dist_from_str = eval(datas)
    # data_base = data_dist_from_str
    # print(data_dist_from_str)
    # print(type(data_dist))
    # data_base = eval(datas)

    # print(datas,len(datas),len(datas[0]))

    # for j in range(len(data_dist_from_str)):
    #     for i in range(len(data_dist_from_str[j])):
    #         print('user data in distt: ', (data_dist_from_str[j][i]))

# print(data_base)
#     print('length ',len(data_base[i]))
#     for i in range(len(data_base)):
        # id = len(data_base[i])
        # print("username : {0}".format(data_base[i]['user']))
        # print("id: {0} username: {1} email: {2} password: {3} phone_number: {4} age: {5}".format(len(data_base[i]),data_base[i]['user'],data_base[i]['email'],data_base[i]['password'],data_base[i]['phone'],data_base[i]['age']))

# readFile.close()

datas = {4: {'email': 'yy@gmail.com', 'u_name': 'yy', 'password': 'password', 'phone': 91212121, 'age': 23}}

key = datas.keys()
value = datas.values()
print(key,value)

def recording_all_data_to_file(data):
    with open("2_assignment.txt",'a') as writeFile:
        writeFile.write(data)
        writeFile.write('\n')
    writeFile.close()


print(len(data_base))

# print(len(dir(dict)))
# for i in range(len(dir(dict))):
#     print("-->", format(dir(dict)[i]))

if __name__ == '__main__':
    recording_all_data_to_file(str([key,value]))

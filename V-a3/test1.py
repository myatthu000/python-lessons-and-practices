db_data: dict = {
    0: {"email": "thu@gmail.com", "name": "thu", "phone": "098888", "address": "86x104", "password": "password"},
    1: {"email": "myat@gmail.com", "name": "myat", "phone": "091111", "address": "86x105", "password": "password"}}

database: dict = {}

def printingData():
    for i in range(len(db_data)):
        print(i, db_data[i])


def create_txt_file():
    try:
        with open('v_test.txt', 'x') as createFile:
            createFile.close()
            print("Text file created successfully.\n")
    except FileExistsError as ferr:
        print("Text file already exit. \n",ferr)

def read_txt_file():
    try:
        with open('v_test.txt','r') as readFile:
            fileText = readFile.readlines()
            # global database
            # database = fileText
            for i in range(len(fileText)):
                # database = fileText[i]
                print(i,fileText[i])
            # print(type(fileText))
            # print(database)
            # print("db = ", type(database))
    except Exception as err:
        print("File Invalid.\n")

def printingDataRaw():
    # global database
    print(database)
# print("db = ", database)

# data1 = '{"email": "thu@gmail.com", "name": "thu", "phone": "098888", "address": "86x104", "password": "password"}'
# print(data1)
# data1.split("'")
# print(data1)
# print(type(data1))


if __name__ == '__main__':
    pass
    printingData()
    # printingDataRaw()
    # create_txt_file()
    # read_txt_file()
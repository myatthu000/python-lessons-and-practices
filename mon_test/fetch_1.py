import pymongo

connection = pymongo.MongoClient('localhost', 27017)
database = connection["ncc_dip2"]
collection = database['user_info']

default_data = {"name":"thu","email":"thu@gmail.com"}
default_data_list = ["thu","thu@gmail.com"]

datas = collection.find({},{"_id":0, "name":1, "email":1, "phone":1})

if collection.count_documents({}) == 0:
    print("no data")
else:
    for i in datas:
        print(i)
        if default_data_list[1] == i['email']:
            print("same ", i['email'])
        # print("Name  :"+i['name'],"Email :"+i['email'],"Phone :"+str(i['phone']))


# dats = {'email':'tt@gmail.com','phone': 75655 }
# print(dats)
# print(dats['email'], dats[1])
ee = str(input("enter something")).lower()
print(ee)
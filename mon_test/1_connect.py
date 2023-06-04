import pymongo
import random

connection = pymongo.MongoClient("localhost",27017)
database = connection['ncc_dip2']
collection = database['user_info']

# data = {"name":"myat","email":"myat@gmail.com"}
#
# ids = collection.insert_one(data)
# print("ids = ",ids.inserted_id)

if __name__ == '__main__':

    while True:
        try:
            user_id = random.randint(10,10000)
            name:str = input("Enter your name:")
            email:str = input("Enter your email:")
            phone:int = int(input("Enter your phone:"))
            password:str = input("Enter your password:")
            data_form = {"_id":user_id,"name":name,"email":email,"phone":phone,"password":password}
            ids = collection.insert_one(data_form)
            print("Inserted :",ids.inserted_id)
        except Exception as err:
            print("err ->",err)
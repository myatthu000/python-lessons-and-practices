import pymongo

import random
connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
collection = database["user_info"]

if __name__ == '__main__':



    for i in range(5):
        user_id = random.randint(10, 10000)
        # name = "Myat"+str(i)
        email: str = "myat"+str(i)+"@gmail.com"
        password: str = "pass"
        phone: int = 94537
        point: int = 100

        info:str = "User data is myat"+str(i)+"id : "+str(user_id)

        # data_form = {"_id": user_id,"name":name, "email": email,"phone": str(phone), "password": password, "info":info}
        data_form = {"_id": user_id, "email": email, "password": password, "phone": str(phone), "info":info, "point":point}

        ids = collection.insert_one(data_form)
        print("inserted id :", ids.inserted_id)
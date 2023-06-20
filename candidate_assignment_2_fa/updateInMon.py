import pymongo

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
candi = database["candidate"]

data_form = {}

for i in candi.find({},{"_id":0,"name":1,"email":1,"info":1,"vote_point":1}):
    # print("datalist : ",i)
    if "ncc9" == i["name"]:
        print("Found user: ")
        i["vote_point"]: int = int(i["vote_point"]) + 1
        data_form.update({"vote_point":i["vote_point"]})

        filter_mon = {"name":i["name"]}
        to_update_db = {"$set":{"vote_point":i["vote_point"]}}
        candi.update_one(filter_mon,to_update_db)

print(data_form)
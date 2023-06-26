import pymongo

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
col = database["user_info"]

candi = database["candidate"]

# # Delete a document
# filter = {"email": "ty@gmail.com"}  # Filter to select the document to delete
#
# result = col.delete_one(filter)
#
# print("Deleted count:", result.deleted_count)
# print("Deleted count:", result)

# data_form = {}
empty_list = []
# data_compare = 0
# id = 0
data = candi.find({}, {"_id": 0, "name": 1, "email": 1, "vote_point": 1})
for i in data:
    to_update = {"name": i["name"], "email": i["email"], "vote_point": i["vote_point"]}
    empty_list.append(to_update)


empty_list = sorted(empty_list, key=lambda x : x["vote_point"], reverse=True)
# print(empty_list)
for i in empty_list:
    print("Name: {} - Vote: {}".format(i['name'],i['vote_point']))

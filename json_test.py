import json

data = '{"email":"thu@gmail.com","pass":"passwordd","phone":33400}'

my_api = json.loads(data)   #str -> json
print(my_api)
print(type(my_api))


my_api = json.dumps(my_api)  #json -> str
print("-->", my_api)
print(type(my_api))

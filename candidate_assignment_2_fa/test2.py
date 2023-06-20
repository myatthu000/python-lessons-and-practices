data = {'message': 'message from accept vote',
        'candi_data': '{"name": "ncc9", "vote_point": 17}',
        'user_data': '{"email": "myat0@gmail.com", "info": "User data is myat0id : 8834", "point": 0}'
        }

# print(data['message'])
# print(data['candi_data'])
# print(data['user_data'])

message, candi_data, user_data = data['message'], data['candi_data'], data['user_data']

print(message)
print(candi_data)
print(user_data)

# for i in candi_data:
#     print()
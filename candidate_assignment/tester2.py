dic_data = {
    0:{'name': 'ncc0', 'vote_point': 0},
    1:{'name': 'ncc1', 'vote_point': 0},
    2:{'name': 'ncc2', 'vote_point': 0},
    3:{'name': 'ncc3', 'vote_point': 0},
    4:{'name': 'ncc4', 'vote_point': 0}
}

data_form = {}
for i in dic_data:
    # print(dic_data[i])
    if 'ncc4' == dic_data[i]["name"]:
        print("found : ", dic_data[i]["name"])
        id = i
        to_update = {id:{'name': dic_data[i]['name'], 'vote_point': dic_data[i]['vote_point']}}
        data_form.update(to_update)
    else:
        print("User not found.")

print(data_form)



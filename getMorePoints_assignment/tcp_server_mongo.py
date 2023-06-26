import socket
import subprocess
import os
import json

import pymongo

'''
    
    
'''

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
col = database["user_info"]

candi = database["candidate"]


class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9998
        self.toSave = {}

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("Server listen on port:{} and ip {}".format(self.server_port, self.server_ip))
        try:
            while True:
                client, address = server.accept()
                print("Accepted Connection from - {} : {} ".format(address[0], address[1]))
                self.handle_client(client)
        except Exception as err:
            print(err)

    def db_update_one(self, collection, filter_name, to_update):
        filter_for_user = filter_name
        to_update_db_for_user = {"$set": to_update}
        collection.update_one(filter_for_user, to_update_db_for_user)

    def get_more_points_server(self, data_list, sock):
        # current_login_user_data = {}
        money = int(data_list[1])
        points = int(data_list[2])
        c_email = data_list[3]
        print("Get More Points :: ", data_list)
        try:

            current_login_user_data = self.email_exit_check(c_email)
            # print("current data : ", current_login_user_data)

            if len(current_login_user_data) != 0:
                print("Work here")
                email = current_login_user_data['email']
                db_money = current_login_user_data['money']
                db_point = current_login_user_data['point']

                # database update for user money
                self.db_update_one(col, {"email": email}, {"money": money})

                # calculation processes
                bought_point = points
                db_point = db_point + bought_point
                db_money = money + db_money
                result_money = db_money - (bought_point * 3)

                # database update for user money after calculation
                self.db_update_one(col, {"email": email}, {"money": result_money})

                # database update for user points
                self.db_update_one(col, {"email": email}, {"point": db_point})

                data_dict = {"_id": 0, "email": 1, "password": 1, "phone": 1, "point": 1, "money": 1}
                data = self.update_db_data_global(email, col, data_dict)
                print("data >>> ", data)
                # data = "User not found"
                str_data = json.dumps(data)
                str_data = bytes(str_data, 'utf-8')
                sock.send(str_data)

            else:
                data = "Get More Point ::User not found"
                print("ddddd", data)
                str_data = json.dumps(data)
                str_data = bytes(str_data, 'utf-8')
                sock.send(str_data)

        except Exception as GPErr:
            print("Get more points server err >>> ", GPErr)

    '''
    This function work for user_info from client to update data 
    '''

    def update_db_data_global(self, c_email, collection, data_dict: dict):
        data_form = {}
        # "_id": 0, "email": 1, "password": 1, "phone": 1, "info": 0, "points": 1, "money": 1}
        for i in collection.find({}, data_dict):
            if c_email == i['email']:
                to_update = i
                data_form.update(to_update)
                break
        return data_form

    def email_exit_check(self, c_email):
        data_store = {}
        try:
            for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "phone": 1, "point": 1, "money": 1}):
                # print("-->", i)
                if c_email == i['email']:
                    to_update = i
                    data_store.update(to_update)
                    break
            print("Email Exit Check >>> ", data_store)
            return data_store
        except Exception as eecErr:
            print("Email exit check >>> ", eecErr)
            return data_store

    def handle_client(self, client_socket):
        data_list = []
        with client_socket as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8").split(' ')  # login email password

            if data_list[0] == "gad":
                print("received command :", data_list[0])
                self.get_all_data(sock)

            elif data_list[0] == "login":
                self.login_checking(sock, data_list)

            elif data_list[0] == "candidate_info":
                self.candidate_info(sock)

            elif data_list[0] == "get_more_points":
                self.get_more_points_server(data_list, sock)

            elif data_list[0] == "Transfer_points":
                self.transfer_points_server(sock, data_list)

            elif data_list[0] == "vote_send":
                self.accept_vote(data_list, sock)

            elif data_list[0] == "Delete_account":
                self.delete_account_server(sock, data_list)

            elif data_list[0] == "Update_user_info":
                self.update_user_info(sock, data_list)

            elif data_list[0] == "voting_ranking":
                self.user_vote_ranking_server(sock, data_list)

            elif data_list[0] == "emailcheck":
                self.email_checking(data_list[1], sock)

            elif data_list[0] == "register":
                self.registration(data_list, sock)

            else:
                sms = bytes("Invalid Option", "utf-8")
                sock.send(sms)

    def user_vote_ranking_server(self, sock, data_list):
        print("Server: Voting Rank >>> ", data_list)
        try:
            ranking_data = self.vote_compare_calc()
            # for i in ranking_data:
            #     print("Name: {} -- Votes: {}".format(i['name'], i['vote_point']))
            sms = json.dumps(ranking_data)
            sock.send(bytes(sms, "utf-8"))
        except Exception as uvErr:
            print("Server: User vote error >>> ", uvErr)

    def vote_compare_calc(self):
        empty_list = []
        data = candi.find({}, {"_id": 0, "name": 1, "email": 1, "vote_point": 1})
        for i in data:
            to_update = {"name": i["name"], "email": i["email"], "vote_point": i["vote_point"]}
            empty_list.append(to_update)

        empty_list = sorted(empty_list, key=lambda x: x["vote_point"], reverse=True)
        # print(empty_list)
        return empty_list

    def update_user_info(self, sock, data_list):
        print("Server: Update user info >>> ", data_list)
        l_email = data_list[1]
        new_value_of_column = data_list[2]
        update_data_column = data_list[3]
        current_user_info = self.email_exit_check(l_email)
        if current_user_info != {}:
            login_email = current_user_info['email']
            self.db_update_one(col, {"email": login_email}, {update_data_column: new_value_of_column})

            data_dict = {"_id": 0, "email": 1, "password": 1, "phone": 1, "info": 1, "point": 1, "money": 1}
            data = self.update_db_data_global(login_email, col, data_dict)
            print("Update current user info", data)
            str_data = json.dumps(data)

            sock.send(bytes(str_data, 'utf-8'))

        else:
            data = "Server :Transfer Points >>> User not found :"
            print(data)
            str_data = json.dumps(data)
            str_data = bytes(str_data, 'utf-8')
            sock.send(str_data)

    def delete_account_server(self, sock, data_list):
        print(data_list)
        l_email = data_list[1]
        current_user_info = self.email_exit_check(l_email)
        if current_user_info != {}:
            login_email = current_user_info['email']
            # Delete a document
            filter_del = {"email": login_email}  # Filter to select the document to delete
            result = col.delete_one(filter_del)
            print("Deleted count:", result.deleted_count)
            print("Deleted c ount:", result)
            if result == 1:
                data = "Delete account successfully."
                str_data = json.dumps(data)
                str_data = bytes(str_data, 'utf-8')
                sock.send(str_data)
            else:
                data = "Account is already deleted."
                str_data = json.dumps(data)
                str_data = bytes(str_data, 'utf-8')
                sock.send(str_data)

    def transfer_points_server(self, sock, data_list):
        print("Server :Transfer Points >>> ", data_list)
        try:
            l_email = data_list[1]
            transfer_email = data_list[2]
            send_point = int(data_list[3])
            current_user_info = self.email_exit_check(l_email)
            transfer_user_info = self.email_exit_check(transfer_email)
            if current_user_info != {} and transfer_user_info != {}:
                l_point = current_user_info['point']
                login_email = current_user_info['email']
                new_l_point = l_point - send_point
                self.db_update_one(col, {"email": login_email}, {"point": new_l_point})

                transfer_email_db = transfer_user_info['email']
                transfer_point_db = transfer_user_info['point']
                new_transfer_point = send_point + transfer_point_db
                self.db_update_one(col, {"email": transfer_email_db}, {"point": new_transfer_point})

                data_dict = {"_id": 0, "email": 1, "password": 1, "phone": 1, "info": 1, "point": 1, "money": 1}
                data1 = self.update_db_data_global(login_email, col, data_dict)
                data2 = self.update_db_data_global(transfer_email_db, col, data_dict)
                print("Server: Transfer {} points from {} to {} successfully".format(send_point, login_email,
                                                                                     transfer_email_db))
                # print("Server: Transfer points complete >>> ", data1)
                # print("Server: Transfer points complete >>> ", data2)
                str_data = json.dumps([data1, data2])
                str_data = bytes(str_data, 'utf-8')
                sock.send(str_data)

            else:
                data = "Server :Transfer Points >>> User not found :"
                print(data)
                str_data = json.dumps(data)
                str_data = bytes(str_data, 'utf-8')
                sock.send(str_data)
        except Exception as TPsErr:
            print("Server :Transfer points Error >>> ", TPsErr)

    def get_all_data(self, sock):
        data: dict = {}
        id = 0
        data_dict = {"_id": 0, "email": 1, "password": 1, "phone": 1, "point": 1, "money": 1}

        for i in col.find({}, data_dict):
            id = len(data)
            # dataform = {"email": i["email"], "password": i["password"], "point": i['point'], "money": i['money']}
            dataform = {"email": i["email"], "password": i["password"], "point": i['point'], "money": i['money']}
            data.update({id: dataform})
        print(data)
        str_data = json.dumps(data)

        str_data = bytes(str_data, 'utf-8')
        sock.send(str_data)

    def login_checking(self, sock, data_list):
        l_email = data_list[1]
        l_password = data_list[2]
        flag = -1
        sms = {}
        for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "info": 1, "point": 1, "money": 1}):
            if i["email"] == l_email and i["password"] == l_password:
                flag = 1
                sms = {"email": i["email"], "info": i["info"], "point": i["point"], "money": i["money"]}
                sms = json.dumps(sms)
                break

        if flag == 1:
            str_data = bytes(sms, 'utf-8')
            sock.send(str_data)
        else:
            str_data = bytes("User name and password not found!", 'utf-8')
            sock.send(str_data)

    def candi_data_update(self, data_list):
        try:
            c_flag = -1
            data_form = {}
            point: int = 0
            for i in col.find({}, {"_id": 0, "name": 1, "email": 1, "info": 1, "point": 1}):
                if i['email'] == data_list[2]:
                    if i['point'] != 0:
                        for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
                            # print("does not match --> ::::: ",i)
                            if i['name'] == data_list[1]:
                                print("Candidate found", i)
                                point = int(i["vote_point"]) + 1

                                to_update = {'name': i["name"], 'vote_point': point}
                                data_form.update(to_update)

                                # database update for candi
                                self.db_update_one(candi, {"name": data_list[1]}, {"vote_point": point})
                                print("After data update for Candidate")
                                c_flag = 1
                                break
                        break
                    else:
                        print("User does not have enough point to vote: ")
                        # break
                    break
            data_form = json.dumps(data_form)

            print("Data form Candidate >>>> : ", data_form)
            return [c_flag, data_form]
        except Exception as candiErr:
            print("Candidate update data error >>>> ", candiErr)

    def user_data_update(self, data_list):
        try:
            u_flag = -1
            data_form = {}
            point: int
            for i in col.find({}, {"_id": 0, "email": 1, "info": 1, "point": 1, "money": 1}):
                if i['email'] == data_list[2]:
                    if i['point'] != 0:
                        print("User found : ", i)
                        point = i["point"] - 1
                        to_update_data = {"email": i["email"], "info": i["info"], "point": point, "money": i['money']}
                        data_form.update(to_update_data)

                        # database update for user
                        self.db_update_one(col, {"email": data_list[2]}, {"point": point})
                        print("After data update for User")
                        # break
                        u_flag = 1
                    else:
                        print("User does not have enough point to vote: ")
                        # break
                    break
            data_form = json.dumps(data_form)
            print("Data form User >>>> : ", data_form)
            return [u_flag, data_form]
        except Exception as userErr:
            print("User update data error >>>> ", userErr)

    def candidate_info(self, sock):
        try:
            to_send = {}
            for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
                print(i["name"], i["vote_point"])
                id = len(to_send) + 1
                to_update = {id: {"name": i["name"], "vote_point": i["vote_point"]}}
                to_send.update(to_update)

            to_send = json.dumps(to_send)
            sock.send(bytes(to_send, "utf-8"))

        except Exception as err:
            print("candiate db access err:", err)
            sock.send(bytes("candi_db_error", "utf-8"))

    def accept_vote(self, data_list, sock):
        # print("data list", data_list)
        sms = {}

        print("Accept vote from server : ")
        c_pass = self.candi_data_update(data_list)
        if c_pass[0] != -1:
            u_pass = self.user_data_update(data_list)
            if u_pass[0] != -1:
                candi_data = c_pass[1]
                user_data = u_pass[1]
                print("candi : {0} \nuser : {1}".format(candi_data, user_data))
                sms = {"message": "message from accept vote", "candi_data": candi_data, "user_data": user_data}
                sms = json.dumps(sms)
                sock.send(bytes(sms, "utf-8"))

    def email_checking(self, email, sock):
        email_exist = 0
        for i in col.find({}, {"_id": 0, "email": 1}):
            if i["email"] == email:
                email_exist = 1

        if email_exist == 0:  # email not already exist
            sock.send(bytes("notExist", "utf-8"))

        else:
            sock.send(bytes("exist", "utf-8"))

    def registration(self, data_list: list, sock):

        data_form = {"email": data_list[1], "password": data_list[2], "phone": int(data_list[3]), "info": data_list[4],
                     "point": int(data_list[5]), "money": 0}

        ids = col.insert_one(data_form)
        print("Registration success for :", ids.inserted_id)

        sock.send(bytes(str(ids.inserted_id), "utf-8"))


if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()

import socket
import subprocess
import os
import json

import pymongo

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

    def handle_client(self, client_socket):
        data_list = []
        with client_socket as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8").split(' ')  # login email password

            # data_list = ["login","email","password"]

            #     output = subprocess.getoutput("dir")
            #     # result = output.stdout.decode()
            #
            #     # return_valued = os.system(received_data)

            if data_list[0] == "gad":
                print("received command :", data_list[0])
                self.get_all_data(sock)

            elif data_list[0] == "login":
                self.login_checking(sock, data_list)

            elif data_list[0] == "candidate_info":
                self.candidate_info(sock)

            elif data_list[0] == "vote_send":
                self.accept_vote(data_list, sock)
                # print("dt list ", data_list)

            elif data_list[0] == "emailcheck":

                self.email_checking(data_list[1], sock)


            elif data_list[0] == "register":

                self.registration(data_list, sock)


            else:
                sms = bytes("Invalid Option", "utf-8")
                sock.send(sms)

    def get_all_data(self, sock):
        data: dict = {}
        id = 0
        for i in col.find({}, {"_id": 0, "email": 1, "password": 1}):
            id = len(data)
            dataform = {"email": i["email"], "password": i["password"]}
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
        for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "info": 1, "point": 1}):
            if i["email"] == l_email and i["password"] == l_password:
                flag = 1
                sms = {"email": i["email"], "info": i["info"], "point": i["point"]}
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

                                # database update for user
                                filter_for_candidate = {"name": data_list[1]}
                                to_update_db_for_candidate = {"$set": {"vote_point": point}}
                                candi.update_one(filter_for_candidate, to_update_db_for_candidate)
                                print("After data update for Candidate")
                                c_flag = 1
                                break
                        break
                    else:
                        print("User does not have enough point to vote: ")
                        # break
                    break
            data_form = json.dumps(data_form)

            # for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
            #     # print("does not match --> ::::: ",i)
            #     if i['name'] == data_list[1]:
            #         print("Candidate found", i["name"])
            #         # print("--->", i)
            #         point = int(i["vote_point"]) + 1
            #
            #         to_update = {'name': i["name"], 'vote_point': point}
            #         data_form.update(to_update)
            #
            #         # database update for user
            #         filter_for_candidate = {"name": data_list[1]}
            #         to_update_db_for_candidate = {"$set": {"vote_point": point}}
            #         candi.update_one(filter_for_candidate, to_update_db_for_candidate)
            #         print("After data update for Candidate")
            #         c_flag = 1
            #         break
            print("Data form Candidate >>>> : ", data_form)
            return [c_flag, data_form]
        except Exception as candiErr:
            print("Candidate update data error >>>> ",candiErr)

    def user_data_update(self, data_list):
        try:
            u_flag = -1
            data_form = {}
            point: int = 0
            for i in col.find({}, {"_id": 0, "name": 1, "email": 1, "info":1, "point": 1}):
                if i['email'] == data_list[2]:
                    if i['point'] != 0:
                        print("User found : ", i)
                        point = i["point"] - 1
                        to_update_data = {"email": i["email"], "info": i["info"], "point": point}
                        data_form.update(to_update_data)

                        # database update for user
                        filter_for_user = {"email": data_list[2]}
                        to_update_db_for_user = {"$set": {"point": point}}
                        col.update_one(filter_for_user, to_update_db_for_user)
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
                print("candi : {0} \nuser : {1}".format(candi_data,user_data))
                sms = {"message":"message from accept vote","candi_data":candi_data,"user_data":user_data}
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
                     "point": int(data_list[5])}

        ids = col.insert_one(data_form)
        print("Registration success for :", ids.inserted_id)

        sock.send(bytes(str(ids.inserted_id), "utf-8"))


if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()
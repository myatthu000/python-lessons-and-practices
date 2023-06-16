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

            if data_list[0] == "gad":
                print("received command :", data_list[0])
                self.get_all_data(sock)

            elif data_list[0] == "login":
                self.login_checking(sock, data_list)

            elif data_list[0] == "candidate_info":
                self.candidate_info(sock, data_list)

            elif data_list[0] == "vote_send":
                self.vote_accept(sock, data_list)

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
        print(data_list)
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

    def candidate_info(self, sock, data_list):
        print("dataList", data_list)
        try:
            to_send = {}
            for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
                print(i["name"], i["vote_point"])
                id = len(to_send) + 1
                to_update = {id: {"name": i["name"], "vote_point": i["vote_point"]}}
                to_send.update(to_update)

            to_send = json.dumps(to_send)

            sock.send(bytes(to_send, "utf-8"))

            print("dataList", data_list)

        except Exception as err:
            print("candiate db access err:", err)

            sock.send(bytes("candi_db_error", "utf-8"))

    def vote_accept(self, sock, data_list):
        candi_flag = -1
        u_flag = -1

        name_of_candi = data_list[1]
        email_of_l_user = data_list[2]
        point_of_l_user = int(data_list[3])

        print("Data list: ", data_list)
        data_form_for_candi = {}  # for candi
        data_form_for_user = {}  # for candi

        for i in candi.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
            # print(dic_data[i])
            if name_of_candi == i["name"]:
                # print("found : ", i)
                vote_point = int(i['vote_point']) + 1
                point_of_l_user = point_of_l_user - 1
                # id = i
                # to_update = {id: {'name':  i["name"], 'vote_point':  i["vote_point"]}}
                to_update = {'name': i["name"], 'vote_point': vote_point}
                data_form_for_candi.update(to_update)
                json_str_to_send = json.dumps(data_form_for_candi)
                sock.send(bytes(json_str_to_send, "utf-8"))

                candi_flag = 1

        for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "info": 1, "point": 1}):
            if email_of_l_user == i["email"]:
                # print("found user : ", i)
                to_update_user = {"email": i["email"], "info": i["info"], "point": point_of_l_user}
                data_form_for_user.update(to_update_user)


        if candi_flag == -1:
            data = "User not found"
            print(data)
            sock.send(bytes(data, "utf-8"))

        print("User : ",data_form_for_user)
        print("Candidate : ",data_form_for_candi)


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

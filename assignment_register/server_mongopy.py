import random
import socket
import subprocess
import os
import json

import pymongo

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
col = database["user_info"]


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

            #     # return_valued = os.system(received_data)

            if data_list[0] == "gad":
                print("received command :", data_list[0])
                self.get_all_data(sock)

            elif data_list[0] == "login":
                self.login_checking(sock, data_list)

            elif data_list[0].lower() == "reg" or data_list[0].lower() == "register":
                self.register_checking(sock, data_list)

            else:
                sms = bytes("Invalid Option", "utf-8")
                sock.send(sms)

    def get_all_data(self, sock):
        data: dict = {}
        id = 0
        if col.count_documents({}) == 0:
            print("Data is empty.")
        else:
            for i in col.find({}, {"_id": 0, "email": 1, "password": 1}):
                # print("from server :", i)
                id = len(data)
                dataform = {"email": i["email"], "password": i["password"]}
                data.update({id: dataform})
            # print(data)
        print('Get all data work.')
        str_data = json.dumps(data)

        str_data = bytes(str_data, 'utf-8')
        sock.send(str_data)

    def register_checking(self, sock, data_list):
        print("---->", data_list)
        datas = col.find({}, {"_id": 0, "email": 1})
        r_email = data_list[2]
        r_flag = 1
        sms = ''

        if col.count_documents({}) == 0:
            # print("Data is empty")
            pass
        else:
            for i in datas:
                print(i)
                if data_list[2] == i['email']:
                    print("same email", i["email"])
                    r_flag = -1
                    # sms = i["info"]
                    break

        if r_flag == 1:
            user_id = random.randint(10, 10000)
            r_name: str = data_list[1]
            r_phone: int = data_list[3]
            r_password: str = data_list[4]

            # info: str = data_list[5]
            info: str = "User data is " + r_name + str(user_id) + "id : " + str(user_id)

            data_form = {"_id": user_id, "name": r_name, "email": r_email, "phone": r_phone, "password": r_password, "info": info}
            # data_form = {"_id": user_id, "name": name, "email": email, "phone": phone, "password": password, "info": info}

            ids = col.insert_one(data_form)
            print("inserted id :", ids.inserted_id)
            print("Register work.")
            sms = "Create new account successfully.\n"+info
            str_data = bytes(sms, 'utf-8')
            sock.send(str_data)
        else:
            sms = "Account is already register by some user."
            str_data = bytes(sms, 'utf-8')
            sock.send(str_data)

    def login_checking(self, sock, data_list):
        print(data_list)
        l_email = data_list[1]
        l_password = data_list[2]
        flag = -1
        sms = ''
        for i in col.find({}, {"_id": 0, "email": 1, "password": 1, "info": 1}):
            if i["email"] == l_email and i["password"] == l_password:
                flag = 1
                sms = i["info"]

                break

        if flag == 1:
            print("Login work.")
            str_data = bytes(sms, 'utf-8')
            # str_data
            sock.send(str_data)
        else:
            str_data = bytes("User name and password not found!", 'utf-8')
            sock.send(str_data)


if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()

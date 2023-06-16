import socket
import subprocess
import os

import pymongo


class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9998
        self.toSave = {}
        self.cus_command = ['gad']
        self.collection = None
        self.connect_db('localhost', 27017, 'ncc_dip2', 'user_info')


    def connect_db(self, localhost, port, database, collect):
        try:
            connection = pymongo.MongoClient(localhost, port)
            database = connection[database]
            self.collection = database[collect]
            print("Connect to Database")
        except Exception as err:
            print("Fail to connect the database.")

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
        with client_socket as sock:
            from_client = sock.recv(1024)
            received_data = from_client.decode("utf-8")
            # print("Received Data From Client:", received_data)

            print("Running Command : ", received_data)

            try:
                output = subprocess.getoutput("dir")
                # result = output.stdout.decode()

                # return_valued = os.system(received_data)
                print("*****************\n", output)
                print("********************")
            except Exception as err:
                print(err)

            # self.toSave.update(received_data)
            message = "server got it:>" + received_data
            to_send = bytes(message, 'utf-8')
            sock.send(to_send)
            self.command_check(received_data)


    def command_check(self,received_data):
        # count:int = 0
        # datas:list = []
        if received_data.lower() == self.cus_command[0] or received_data.lower() == "get all data":
            print("-" * 50, '\n')
            print("You typed command \"{0}\"".format(received_data))
            print("-" * 50)
            try:
                datas = self.collection.find({}, {"_id": 0, "name": 1, "email": 1, "phone": 1})
                # print("--->",type(datas))
                count = self.collection.count_documents({})
                if count == 0:
                    print("Data is Empty. Please Fill data first.")
                else:
                    for i in datas:
                        print("[Name] :" + i['name'], "[Email] :" + i['email'], "[Phone] :" + str(i['phone']))
                print("-" * 50, '\n')
            except Exception as err:
                print("Connection error\n", err)










if __name__ == '__main__':
    tcpserver = TCPserver()
    tcpserver.main()

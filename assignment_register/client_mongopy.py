import socket
import json


class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9998
        self.input_checking(sms)

    def client_runner(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))

        # client.send(self.client_sms)
        #
        #     received_from_server = client.recv(4096)
        #
        #     recv_sms = received_from_server.decode("utf-8")
        #
        #     print("$:", recv_sms)
        #
        #     client.close()
        return client  # to send and received data

    def input_checking(self, sms):
        if sms == "gad":
            self.get_all_data(sms)

        elif sms == "login":
            self.login(sms)

        elif sms.lower() == "reg" or sms.lower() == "register":
            self.register(sms)
        else:
            print("Invalid Option")

    def get_all_data(self, sms):
        client = self.client_runner()
        sms = bytes(sms + ' ', "utf-8")
        client.send(sms)
        received_from_server = client.recv(4096)
        # print(received_from_server.decode("utf-8"))
        dict_data: dict = json.loads(received_from_server.decode("utf-8"))
        print(type(dict_data))
        if dict_data == {}:
            print("Data is empty")
        else:
            # print(dict_data)
            for i in dict_data:
                print(dict_data[i])

        client.close()

    def login(self, info):
        try:
            print("This is login Form")
            l_email = input("Enter your email to login:")
            l_pass = input("Enter your password to login:")

            client = self.client_runner()
            sms = info + ' ' + l_email + ' ' + l_pass  # login email password
            sms = bytes(sms, "utf-8")
            client.send(sms)
            received_from_server = client.recv(4096)
            print(received_from_server.decode("utf-8"))
            client.close()

        except Exception as err:
            print(err)

    def register(self, info):
        r_c_pass = True
        print("This is registration Form ")
        try:
            r_name = input("Enter your name to register:")
            r_email = str(input("Enter your email to register:"))
            r_phone = input("Enter your phone number to register:")

            while r_c_pass:
                r_password: str = str(input("Enter your password to register:"))
                c_password: str = str(input("Confirm your password to register:"))
                if r_password == c_password:
                    client = self.client_runner()
                    # info:str = "User data is "+ r_name + str(user_id) + "id : "+str(user_id)
                    sms = info + ' ' + r_name + ' ' + r_email + ' ' + r_phone + ' ' + r_password  # login email password
                    sms = bytes(sms, "utf-8")
                    # print("\n Send from client: {0} \n".format(sms))
                    client.send(sms)
                    received_from_server = client.recv(4096)
                    received_from_server = received_from_server.decode("utf-8")
                    print(received_from_server)
                    client.close()
                    # if not received_from_server["register_checking"]:
                    #     self.input_checking(sms)
                    break

        except Exception as err:
            print("error at register : -->\n",err)


if __name__ == "__main__":
    while True:
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)
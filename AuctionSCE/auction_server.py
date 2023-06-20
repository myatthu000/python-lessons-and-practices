import socket


class Server:
    def __init__(self):
        self.server_ip = "localhost"
        self.server_port = 65521

    def main(self):
        auction_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auction_server.bind((self.server_ip, self.server_port))
        auction_server.listen()
        print("Server listen on port:{} and ip:{}".format(self.server_port, self.server_ip))
        try:
            while True:
                # accept
                client, address = auction_server.accept()
                print("Connection accepted at >>> {} : {} ".format(address, client))
                self.client_control(client)

        except Exception as mErr:
            print("Error at Main : ", mErr)

    # client_control/socket/handle_client

    def client_control(self, client):
        with client as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8").split(' ')
            print("Data List >>> ", data_list)

            sock.send(bytes("Connection from server Successfully.","utf-8"))


if __name__ == '__main__':
    auction = Server()
    auction.main()

import socket
import encry_decrypt


class Auction_Client():
    def __init__(self):
        self.target_ip = "localhost"
        self.traget_port = 65521
        self.encryption()

    def client_runner(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.traget_port))

        return client  # to run and received data

    def client_menu(self):
        print(">>> This is client ment <<<")
        user_data = input("Press 1 to send data : ")

        client = self.client_runner()

        client.send(bytes(user_data, "utf-8"))

        # recv from server
        received_from_server = client.recv(4096)
        received_from_server = received_from_server.decode("utf-8")
        print("Received from server >>> ", received_from_server)

    def encryption(self):
        userKey: str = input("Enter your encryption key for the whole process : ")
        encry = encry_decrypt.A3Encryption()
        encrypted_data = encry.start_encryption("NationalCyberCity",userKey)
        print(encrypted_data)


if __name__ == '__main__':
    auction_client = Auction_Client()
    # auction_client.client_runner()
    while True:
        auction_client.client_menu()

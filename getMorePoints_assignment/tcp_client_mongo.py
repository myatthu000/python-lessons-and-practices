import socket
import json

'''
    Assignment 8
    
'''


class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9998
        self.input_checking(sms)
        global user_info

    def client_runner(self):

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client  # to send and received data

    def input_checking(self, sms):
        if sms == "gad":
            self.get_all_data(sms)

        elif sms == "login":
            self.login(sms)

        elif sms == "reg":
            self.register()
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
        print(dict_data)
        client.close()

    def login(self, info):
        try:
            # global user_info
            print("This is login Form")
            l_email = input("Enter your email to login:")
            l_pass = input("Enter your password to login:")

            client = self.client_runner()
            sms = info + ' ' + l_email + ' ' + l_pass  # login email password
            sms = bytes(sms, "utf-8")
            client.send(sms)
            received_from_server = client.recv(4096)
            user_info: dict = json.loads(received_from_server.decode("utf-8"))
            # user_info = user_info.update(user_info_data)
            print("login >>> ", user_info)
            self.option_choice(user_info, client)

        except Exception as err:
            print(err)

    def option_choice(self, user_info, client):
        print(">>>>>>>>>>>>>>>> This is Option Choice <<<<<<<<<<<<<<<<")
        # print("option choice",user_info)
        print("Email :", user_info["email"])
        print("Info :", user_info["info"])
        print("Point :", user_info["point"])

        try:
            option = input("Press 1 to Get User Option:\nPress 2 To Get Main Option:\nPress 3 To Exit:")
            if option == '1':
                self.user_option(user_info, client)
            elif option == '2':

                # self.input_checking("from_option")  # to write more option
                sms = input("Enter some data to send:")
                self.input_checking(sms)
            elif option == '3':
                exit(1)
            else:
                print("Invalid Option [X]")
                self.option_choice(user_info, client)

        except Exception as err:
            print(err)

    def user_option(self, user_info, client):
        print(">>>>>>>>>>>>>>>> This is User Option <<<<<<<<<<<<<<<<")
        try:
            option = input("Press 1 To Vote:\nPress 2 to get more points:\nPress 3 to Transfer Point:\n"
                           "Press 4 To get Voting Ranking:\nPress 5 to change user information \nPress 6 to Delete Acc:\nPress 7 "
                           "to Exit: \nPress 8 to go back")

            if option == '1':
                self.voting(user_info)
                self.send_vote(user_info, client)
            elif option == '2':
                self.get_more_points(user_info, client)
            elif option == '3':
                self.transfer_points(user_info, client)
            elif option == '4':
                self.user_vote_ranking_client(user_info, client)
            elif option == '5':
                self.update_user_info(user_info, client)
            elif option == '6':
                self.delete_account_client(user_info, client)
            elif option == '7':
                exit(1)
            elif option == '8':
                self.option_choice(user_info, client)

            else:
                print("Invalid option")
                self.user_option(user_info, client)

        except Exception as err:
            print(err)
            self.user_option(user_info, client)

    def user_vote_ranking_client(self, user_info, client):
        try:
            l_email = user_info['email']
            client = self.client_runner()
            sms = "voting_ranking"+' '+l_email
            client.send(bytes(sms,"utf-8"))

            recv = client.recv(4096)
            data = json.loads(recv.decode("utf-8"))
            print("Voting Ranks.\nRanking Lists order by descending ::: ")
            j = 0
            for i in data:
                j += 1
                print("No: {} -- Name: {} -- Email: {} -- Votes: {}".format(j, i['name'], i['email'], i['vote_point']))

            client.close()
            self.user_option(user_info, client)

        except Exception as uvErr:
            print("Client: User voting ranking error >>> ",uvErr)

    def update_user_info(self, user_info, client):
        update_data = ""
        update_data_flag = -1
        try:
            print(" >>>>>>>>>> Update User Information <<<<<<<<<< ")
            l_email = user_info['email']
            update_data_columns = str(input("Choose user columns to update >>>\npassword :"
                                       "\nphone :\ninfo :")).lower()

            if update_data_columns == "password":
                password = str(input("Enter new password: "))
                confirm_password = str(input("Retype password to confirm: "))
                if password == confirm_password:
                    update_data = password
                    print("Client: Password match.")
                    update_data_flag = 1

                else:
                    print("Client: Password does not match. Try again.")
                    self.update_user_info(user_info, client)

            elif update_data_columns == "phone":
                phone = str(input("Enter new phone number: "))
                update_data = phone
                update_data_flag = 1

            elif update_data_columns == "info":
                info = str(input("Enter user info to update: "))
                update_data = info
                update_data_flag = 1

            elif update_data_columns == "email":
                print("You cannot update email:")
                self.update_user_info(user_info, client)

            else:
                print("Invalid choice : ")
                self.update_user_info(user_info, client)

            if update_data_flag == 1:
                sms = "Update_user_info" + ' ' + l_email + ' ' + update_data + ' ' + update_data_columns
                client = self.client_runner()
                client.send(bytes(sms, "utf-8"))

                recv = client.recv(4096)
                data = json.loads(recv.decode("utf-8"))
                # if len(recv) != 0:
                user_info = data
                client.close()
                print("Client: Update user info >>> ", user_info)
                self.user_option(user_info, client)

        except Exception as uiErr:
            print("Update user info : ", uiErr)

    def delete_account_client(self, user_info, client):
        try:
            confirmation_delete = str(input("Are you sure to delete your account [y/n]"))
            l_email = user_info['email']
            if confirmation_delete == 'y' or confirmation_delete == 'Y':
                your_email = str(input("Retype your email to confirmed"))
                if your_email == l_email:
                    print(">>>>>>>> Account deletion confirmed <<<<<<<<")
                    client = self.client_runner()
                    sms = "Delete_account" + ' ' + l_email
                    client.send(bytes(sms, "utf-8"))

                    # recv
                    recv = client.recv(4096)
                    data = json.loads(recv.decode("utf-8"))
                    print(data)

                    client.close()
                    sms = input("Enter some data to send:")
                    self.input_checking(sms)
                else:
                    print("Try again. Your email does not match. ")
                    self.delete_account_client(user_info, client)
            elif confirmation_delete == 'n' or confirmation_delete == 'N':
                print(">>>>>>>> Account deletion cancel <<<<<<<<")
                self.user_option(user_info, client)
            else:
                print("Invalid Choice.")
                self.delete_account_client(user_info, client)

        except Exception as delErr:
            print("Delete account Error >>> ", delErr)

    def transfer_points(self, user_info, client):
        try:
            l_email = user_info['email']
            l_points = user_info['point']
            if l_points != 0:
                print("You have enough points to Transfer >>> ", l_points)
                transfer_email = str(input("Enter email to Transfer >>> "))
                if transfer_email != user_info['email']:
                    send_points = int(input("Enter amount of points to Transfer >>> "))
                    if send_points > l_points:
                        print("Your transfer points is out of your own amount : ")
                        self.user_option(user_info, client)
                    else:
                        client = self.client_runner()
                        sms = "Transfer_points" + ' ' + l_email + ' ' + transfer_email + ' ' + str(send_points)
                        client.send(bytes(sms, "utf-8"))

                        recv = client.recv(4096)
                        data = json.loads(recv.decode("utf-8"))
                        if len(data) > 0:
                            user_info = data[0]
                            print("Client: Transfer point >>> ", user_info)
                        else:
                            print("Something wrong in data receiver >>> ")

                else:
                    print("LOL ,You cannot transfer point yourself ;( ")

                client.close()
                self.user_option(user_info, client)
            else:
                print("You don't have enough points to transfer. \nPlease buy first >>> ", l_points)
                self.user_option(user_info, client)
        except Exception as TPErr:
            print("Client : Transfer Point Error >>> ", TPErr)
            self.user_option(user_info, client)

    def get_money(self, user_info):
        money: int
        l_money = user_info['money']
        if l_money > 6:
            money = l_money
        else:
            money: int = int(input("Enter money to buy points : $ "))
        return money

    def get_more_points2(self, user_info, client):
        print("User info >>> ",user_info)
        l_email = user_info['email']
        l_amount = user_info['money']
        str(input("Enter "))
        current_fill_amount = int(input("Enter amount of money to buy points. "))


    def get_more_points(self, user_info, client):
        print("User info >>> ", user_info)
        l_email = user_info['email']
        update_user_info = ''
        try:
            money = self.get_money(user_info)
            print("Your amount of money is >>> :", money)
            # money: int = int(input("Enter money to buy points : $ "))
            if money <= 3:
                self.get_more_points(user_info, client)
            else:
                points = int(input("Enter Points to vote:\n*** 1 points 3 dollars >>> "))
                client = self.client_runner()
                sms = "get_more_points" + ' ' + str(money) + ' ' + str(points) + ' ' + l_email
                client.send(bytes(sms, "utf-8"))

                recv = client.recv(4096)
                data = json.loads(recv.decode("utf-8"))
                print("Send vote method work : >>>> ")
                if len(recv) > 0:
                    print(data)
                    print("Type ", data)
                    user_info = data

                client.close()
                self.user_option(user_info, client)
        except Exception as gError:
            print("Get more point error :{}".format(gError))
            self.get_more_points(user_info, client)

    def voting(self, user_info):
        client = self.client_runner()
        sms = bytes("candidate_info", "utf-8")
        client.send(sms)

        info = client.recv(4096)
        candi_info = json.loads(info.decode("utf-8"))
        print("Candidate info >>>> ", candi_info)
        print(type(candi_info))
        for i in candi_info:
            print("No: ", i, "Name: ", candi_info[i]["name"], "Point", candi_info[i]["vote_point"])

        print("Voting method work : ")
        client.close()

    def send_vote(self, user_info, client):
        try:
            if user_info['point'] != 0:
                client = self.client_runner()
                user_vote = str(input("Enter candidate name to vote : "))
                to_send_email = user_info['email']

                sms = bytes("vote_send" + " " + user_vote + " " + to_send_email, "utf-8")
                client.send(sms)
                # print("Send from client sms", sms)

                received_message_from_server = client.recv(4096)
                data = json.loads(received_message_from_server.decode("utf-8"))
                print("Send vote method work : >>>> ")
                # print("Send vote method work : >>>> ", data)
                message, candi_data, user_data = data['message'], json.loads(data['candi_data']), json.loads(
                    data['user_data'])

                # print("message :::::::::::::::: ", message)
                print("\ncandi_data :::::::::::::::: ", candi_data)
                print("user_data :::::::::::::::: ", user_data, '\n')

                user_info = user_data
                print("User Info : ", user_info)

                self.option_choice(user_info, client)
            else:
                print("User does not have enough point to vote:\n:::::::::::\nPlease buy points first: ", user_info)
                self.user_option(user_info, client)

        except Exception as sErr:
            print("Send Vote err : ", sErr)
            self.voting(user_info)
            self.send_vote(user_info, client)

    def register(self):
        print("\nThis is registration option ")
        r_email = ''
        while True:
            r_email = input("Enter email for registration :")
            flag = self.email_checking(r_email)  # 1 or -1

            if flag == 1:
                break
            else:
                print("Email Form Invalid\nTry Again! ")

        print("Email From Valid ")

        try:
            option = input("Press 1 Registration for Voter:\nPress 2 Registration for Candidate!:")

            if option == '1':
                self.reg_for_voter(r_email)
            elif option == '2':
                pass

            else:
                self.register()
        except Exception as err:
            print(err)

    def email_checking(self, r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        print("Name counter: ", name_counter)

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # print(email_name)
        print(email_form)

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (ord(aChar) > 31 and ord(aChar) < 48) or (ord(aChar) > 57 and ord(aChar) < 65) or (
                    ord(aChar) > 90 and ord(aChar) < 97) or (ord(aChar) > 122 and ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):

            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1

        else:
            return 1

    def reg_for_voter(self, r_email):

        if self.email_check_inDB(r_email):
            try:
                pass1 = input("Enter your password to register:")
                pass2 = input("Enter your password Again  to register:")

                if pass1 == pass2:

                    print("Password Was match!")
                    phone = int(input("Enter your phone number:"))

                    data_list = [r_email, pass1, phone]
                    self.final_registration(data_list)

                else:
                    print("Password not match:")
                    self.reg_for_voter(r_email)


            except Exception as err:
                print(err)

        else:

            print("Your email was already register!")
            self.register()

    def email_check_inDB(self, email):

        client = self.client_runner()
        data = "emailcheck" + " " + email

        client.send(bytes(data, "utf-8"))

        received = client.recv(4096).decode("utf-8")

        print(received)

        if received == "notExist":
            client.close()
            return True
        else:
            client.close()
            return False

    def final_registration(self, data_list):

        data_form = "register" + " " + data_list[0] + " " + data_list[1] + " " + str(
            data_list[2]) + " " + "User" + " " + "100"

        client = self.client_runner()

        client.send(bytes(data_form, "utf-8"))

        recv = client.recv(4096).decode("utf-8")

        print(recv)

        if recv:
            print("Registration Success!", recv)
            info = "login"
            self.login(info)

        client.close()


if __name__ == "__main__":
    while True:
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)

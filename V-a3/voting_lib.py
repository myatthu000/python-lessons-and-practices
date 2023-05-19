class Voting:
    def __init__(self):
        print("Working in Voting special method or constructor ")
        self.students = {0: {"name": "James", "v_mark": 0, "voter": [], "student_points" : 0},
                         1: {"name": "John", "v_mark": 0, "voter": [], "student_points" : 0},
                         2: {"name": "Rooney", "v_mark": 0, "voter": [], "student_points" : 0},
                         3: {"name": "Ronaldo", "v_mark": 0, "voter": [], "student_points" : 0},
                         4: {"name": "Messi", "v_mark": 0, "voter": [], "student_points" : 0}
                         }
        db_data: dict = {0: {"email": "thu@gmail.com", "name": "thu", "phone": "098888", "address": "86x104", "password": "password"},
                         1: {"email": "myat@gmail.com", "name": "myat", "phone": "091111", "address": "86x105", "password": "password"}}
        self.db: dict = {}
        # self.db.update(db_data)
        self.id: int = 0

        self.l_id: int = 0

    def main_option(self):
        option = 0
        try:
            option = int(input("Press 1 to Register\nPress 2 to Login\nPress 3 to Exit"))
        except Exception as err:
            # print(err)
            print("Pls insert only Integer eg:1,2,3")

        if option == 1:
            self.register()
        elif option == 2:
            self.login()
        elif option == 3:
            exit(1)
        else:
            print("Invalid Option")
            self.main_option()

    def register(self):
        print("This is register option ")
        pass_match = False
        try:
            r_email = input("Enter your email address to register!")
            r_name = input("Enter your name to register!")
            r_phone = input("Enter your phone to register!")
            r_address = input("Enter your address:")

            while pass_match is False:
                r_pass1 = input("Enter your password to register!")
                r_pass2 = input("Retype your password:")

                if r_pass1 != r_pass2:
                    print("Your passwords not match")

                else:
                    print("Your passwords was recorded!")

                    self.id = len(self.db)
                    data_form: dict = {self.id: {"email": r_email, "name": r_name, "phone": r_phone,
                                                 "address": r_address, "password": r_pass1,"show_money":None,"points":None}}

                    self.db.update(data_form)
                    print("db == \n",self.db)

                    pass_match = True

            showMoney = False
            while pass_match is True:
                show_money = int(input("Enter your show money: "))
                if show_money > 10:
                    print("===" * 20, "\n")
                    points = int(input("1 point = 10 $\nBuy points to vote students:\n"))
                    if points != 0:
                        used_money = points * 10
                        show_money = show_money - used_money
                        print("You buy {0} points for {1} $\n Your show money:{2}".format(points, used_money,show_money))

                        # self.id = len(self.db)
                        data_form: dict = {self.id: {"email": r_email, "name": r_name, "phone": r_phone,
                                                     "address": r_address, "password": r_pass1,
                                                     "show_money": show_money, "points": points}}

                        self.db.update(data_form)
                        print("--->\n",self.db)
                        break
                else:
                    print("Your money is very low. Money show be above 10 $.\n")

                    # showMoney = True
        except Exception as err:
            print("Invalid User Input!Try Again Sir!")
            self.register()

    # def buying_option(self):
    #     print("Enter ")

        print("Registration success :", self.db[self.id]["name"])

        r_option = False
        while r_option is False:
            try:
                user_option = int(input("Press 1 to Login!\nPress 2 Main Option:\nPress3 to Exit!:"))
                if user_option == 1:
                    self.login()
                    break
                elif user_option == 2:
                    self.main_option()
                    break
                elif user_option == 3:
                    exit(1)
                else:
                    print("Pls read again for option!")

            except Exception as err:
                print("Invalid Input!", err)

    def login(self):
        print("This is login option ")
        length = len(self.db)
        try:
            l_email = input("Enter your email to Login:")
            l_pass = input("Enter your pass to Login:")
            self.l_id = -1
            for i in range(length):
                if l_email == self.db[i]["email"] and l_pass == self.db[i]["password"]:
                    self.l_id = i
                    break
            if self.l_id != -1:
                self.user_sector(self.l_id)
            else:
                print("Username or Password incorrect!")
                self.login()

        except Exception as err:
            print(err, "\nInvalid input:")

    def printingAllData(self):
        try:
            print("\nData: \n{0}".format(self.db))
            print("\nVoting Students: \n{0}".format(self.students))
        except Exception as err:
            print(err)

    def user_sector(self, l_id):
        print("Welcome", self.db[l_id]["name"])

        print("Please select one!")
        for i in range(len(self.students)):
            print("Id:{} - Name {} - Current Vote Mark: {}".format(i, self.students[i]["name"],
                                                                   self.students[i]["v_mark"]
                                                                   ))

        try:
            v_id = int(input("Just Enter Id number to vote:"))

            self.students[v_id]["v_mark"] += 1

            self.students[v_id]["voter"].append(self.db[l_id]["name"])

            print("Congratulation you are voted!")
            print("{} now voting mark is : {}".format(self.students[v_id]["name"],self.students[v_id]["v_mark"]))

            for i in range(len(self.students[v_id]["voter"])):
                print("Voter: ", self.students[v_id]["voter"][i])

            # from db
            points = self.db[l_id]["points"]
            user_id = self.db[l_id]
            
            result_points = points - 1
            self.students[v_id]["student_points"] = self.students[v_id]["student_points"] + 1
            student_points = self.students[v_id]["student_points"]

            print("points {0} user_id {1} student_points {2}".format(result_points,l_id,student_points))

        except Exception as err:
            print(err)


        while True:
            try:
                self.printingAllData()
                vote_option = int(input("Press 1 to Vote Again!\nPress 2 to get Main Option!\nPress 3 to Force Quit:"))

                if vote_option == 1:
                    self.user_sector(l_id)
                    break
                elif vote_option == 2:
                    self.main_option()
                    break
                elif vote_option == 3:
                    exit(1)
                else:
                    print("Invalid option after vote!")
            except Exception as err:
                print(err)



# ဆက်ရေး ရန် 8-5-2023
# voter များအား စာရင်း မှတ်ပေးရန်
# file ထဲ တွင် အားလုံး သိမ်းရန်
#
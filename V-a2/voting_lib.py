class Voting:
    def __init__(self):
        print("Working in Voting special method or constructor ")
        self.students = {0: {"name": "James", "v_mark": 0, "voter": [], "std_points": 0},
                         1: {"name": "John", "v_mark": 0, "voter": [], "std_points": 0},
                         2: {"name": "Rooney", "v_mark": 0, "voter": [], "std_points": 0},
                         3: {"name": "Ronaldo", "v_mark": 0, "voter": [], "std_points": 0},
                         4: {"name": "Messi", "v_mark": 0, "voter": [], "std_points": 0}
                         }
        self.db: dict = {}
        self.id: int = 0

        self.l_id: int = 0
        self.money: int =0
        self.points: int =0

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
                    pass_match = True

                    if pass_match is True:
                        self.showMoney_points()

                        data_form: dict = {self.id: {"email": r_email, "name": r_name, "phone": r_phone,
                                                     "address": r_address, "password": r_pass1,"show_money": int(money), "points": int(points)}}

                        self.db.update(data_form)

                        self.printingAllData()
                        print("-------\n")
                        self.single_printing_function(self.id)
        except Exception as err:
            print("Invalid User Input!Try Again Sir!")
            self.register()

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


    def showMoney_points(self):
        try:
            global money, points
            show_money : str = ""
            buy_points : str = ""

            showMoney = False
            buyPoints = False

            while showMoney is False:
                show_money = input("Enter your show money: ")
                if int(show_money) <= 10 or int(show_money) > 1000000:
                    print("Invalid Amounts")
                else:
                    print("Valid Amounts, you can buy some points to vote:")
                    money = show_money
                showMoney = True
                break

            while buyPoints is False:
                try:
                    buy_points = input("Buy points to vote:\n1 Points 5 $:")
                    pay_price = int(buy_points) * 5
                    after_buy_points_money = int(show_money) - pay_price

                    if after_buy_points_money < 0:
                        print("You don't have enough money to buy points to vote:\n")
                    else:
                        print("You bought points {0} for {1} $.\nYour balance is now {2} $".format(buy_points, pay_price, after_buy_points_money))

                        buyPoints = False
                        money = after_buy_points_money
                        points = buy_points
                    break
                except Exception as err2:
                    print("--------",err2)

            # return [show_money,buy_points]
        except Exception as errsp:
            print("Invalid Option:...........",errsp)
            self.showMoney_points()


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
        for i in range(len(self.db)):
            print(self.db[i])
            # print("id :{0} - name :{1} - email :{2} - money :{3} - points :{4} - phone-no :{5} - password :{6}".format(self.db[i]["id"],self.db[i]["name"],self.db[i]["email"],self.db[i]["money"],self.db[i]["points"],self.db[i]["phone"],self.db[i]["password"]))
        # print("Database :{} \n".format(self.db))


    def printingAllStudents(self):
        for i in range(len(self.students)):
            print("Id:{} - Name {} - Current Vote Mark: {} - Voter: {} - Student Points {}".format(i, self.students[i]["name"],
                                                                   self.students[i]["v_mark"], self.students[i]["voter"], self.students[i]["std_points"],
                                                                   ))


    def single_printing_function(self, l_id):
        try:
            user = self.db[l_id]
            print(user)
            # print("id :{0} - name :{1} - email :{2} - money :{3} - points :{4} - phone-no :{5}".format(user["id"],user["name"],user["email"],user["money"],user["points"],user["phone"]))
            # print("\nYou vote this students :\nname: {}, v_mark: {}, voter: {}".format(user["id"],user["name"],user["email"],user["money"],user["points"],user["phone"]))
        except Exception as errspf:
            print("Error at -->",errspf)

    def after_vote_points_to_stds(self,v_id,l_id):
        try:
            # voter id, name, points

            user_id = l_id

            points_of_user = self.db[user_id]["points"]
            if points_of_user <= 0:
                print("You don't have enough to points to vote students\nPlease buy points to vote, Thanks\n")
                self.main_option()
            else:
                self.db[user_id]["points"] = int(int(self.db[user_id]["points"]) - 1)
                self.students[v_id]["std_points"] = int(int(self.students[v_id]["std_points"]) + 1)
                original_points = int(self.db[user_id]["points"])
                std_points = self.students[v_id]["std_points"]

                name = self.db[user_id]["name"]  # voter

                # students
                std_name = self.students[v_id]["name"]

                print("voter :{0}\nresult points :{1}\nstudents :{2}\nstudent points {3}\n".format(name, original_points, std_name, std_points))

        except Exception as erravp:
            print("Error --->",erravp)



    def user_sector(self, l_id):
        print("Welcome", self.db[l_id]["name"])

        points_of_user = self.db[l_id]["points"]
        if points_of_user <= 0:
            print("You don't have enough points to vote students\nPlease buy points to vote, Thanks\n")
            # self.printingAllData()
            self.single_printing_function(self.l_id)
            self.main_option()
        else:
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
                    print("Voter: ",self.students[v_id]["voter"][i])

                self.after_vote_points_to_stds(v_id, self.l_id)

                print("\n")
                self.printingAllStudents()
            except Exception as err:
                print(err)


            while True:
                try:
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
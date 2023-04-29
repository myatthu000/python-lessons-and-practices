def mgmg():
    print("I am mgmg")
    print("I am 10 years old")
    print("I am programmer.")


def aung_aung():
    print("I am aung aung")
    print("I am 20 years old")
    print("I am pro-programmer.")


name = input("enter name ")

def run():
    while(name):
        if name == 'mgmg':
            mgmg()
            # break
        elif name == "aungaung":
            aung_aung()
            # break
        else:
            print("Invalid option")
        break
run()
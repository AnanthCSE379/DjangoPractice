from p4 import Spanner,Scissor,ScrewDriver


class Toolslist():
    def __init__(self):
        self.tools = []
    def main(self):
        print("Enter the details for Spanner :")
        sp_s = int(input("Enter the strength of spanner : "))
        sp_size = int(input("Enter the size of spanner : "))
        sp = Spanner("Spanner",sp_s,sp_size)
        print("Enter the details for Scissor :")
        sc_s = int(input("Enter the strength of scissors : "))
        sc_length = int(input("Enter the length of the scissors : "))
        sc = Scissor("Scissors",sc_s,sc_length)
        print("Enter the details for Screw Driver :")
        sd_s = int(input("Enter the strength of screw driver : "))
        sd_toothsize = int(input("Enter the toothsize of screw driver : "))
        sd = ScrewDriver("ScrewDriver",sd_s,sd_toothsize)

        print(sp)
        print(sc)
        print(sd)

tl = Toolslist()
tl.main()

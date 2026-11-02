from p3 import Tool
from p2 import InvalidException
class Spanner(Tool):
    def __init__(self,typee,strength,size):
        self.__size=size
        super().__init__(typee,strength)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self,size):
        try:
            if size<5 or size>15:
                raise InvalidException("Invalid size of spanner")
            self.__size = size
        except InvalidException as e:
            print(e)

    def __str__(self):
        s=super().__str__()
        s1=s+"\nSize : "+str(self.__size)
        return s1
            

class ScrewDriver(Tool):
    def __init__(self,typee,strength,toothsize):
        self.__toothsize=toothsize
        super().__init__(typee,strength)

    @property
    def toothsize(self):
        return self.__toothsize

    @toothsize.setter
    def toothsize(self,__toothsize):
        try:
            if toothsize < 20 or toothsize > 40:
                raise InvalidException("Toothsize beyond bounds")
            self.__toothsize=toothsize
        except InvalidException as e:
            print(e)
    def __str__(self):
        s = super().__str__()
        s1 = s+"\nToothSize : "+str(self.__toothsize)
        return s1


class Scissor(Tool):
    def __init__(self,typee,strength,length):
        self.__length=length
        super().__init__(typee,strength)

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self,length):
        try:
            if length<0 or length>12:
                raise InvalidException("Length beyond bounds")
            self.__length=length
        except InvalidException as e:
            print(e)
    def __str__(self):
        s = super().__str__()
        s1 = s + "\nLength : "+str(self.length)
        return s1
            
            
    


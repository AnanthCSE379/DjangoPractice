class Student():
    def __init__(self,regno,name,sub1,sub2,sub3):
        self.__regno=regno
        self.__name=name
        self.__sub1=sub1
        self.__sub2=sub2
        self.__sub3=sub3
        self.__total=sub1+sub2+sub3
        self.grade=''

    @property
    def regno(self):
        return self.__regno

    @property
    def grade(self):
        return self.__grade

    @grade.setter
    def grade(self,grade):
        self.__grade=grade

    def showDetail(self):
        print(self)

    def computeGrade(self):
        avg=self.__total/3
        if (avg>=90):
            self.grade='s'
        elif (avg>80):
            self.grade='a'
        elif (avg>70):
            self.grade='b'
        elif (avg>60):
            self.grade='c'
        elif (avg>50):
            self.grade='d'
        else:
            self.grade='f'

    def checkForScholarship(self):
        if (self.grade=='s'):
            return "eligible"
        else:
            return "not eligible"

    def __str__(self):
        return ("Name : " + str(self.__name) +
                "\nRegister No : " + str(self.__regno) +
                "\nSubject1 Marks : " + str(self.__sub1) +
                "\nSubject2 Marks : " + str(self.__sub2) +
                "\nSubject3 Marks : " + str(self.__sub3) +
                "\nTotal : " + str(self.__total) +
                "\nGrade : " + self.grade)


class SpecialCourse():
    def __init__(self,cred,strength):
        self.credit=cred
        self.strength=strength

    def display(self):
        print("Course Details : ")
        print("Credits : ",self.credit)
        print("Strength : ",self.strength)


class PythonCourse(SpecialCourse):
    def __init__(self,cred,strength,lst):
        super().__init__(cred,strength)
        self.lst=list(lst)

    def display(self):
        print("\nPython Course")
        super().display()
        for i in self.lst:
            print(i)

    def storeTextFile(self):
        with open("details.txt","a") as fobj:
            fobj.write("\nPython Course\n")
            for i in self.lst:
                fobj.write(str(i)+"\n\n")


class JavaCourse(SpecialCourse):
    def __init__(self,cred,strength,lst):
        super().__init__(cred,strength)
        self.lst=list(lst)

    def display(self):
        print("\nJava Course")
        super().display()
        for i in self.lst:
            print(i)

    def storeTextFile(self):
        with open("details.txt","a") as fobj:
            fobj.write("\nJava Course\n")
            for i in self.lst:
                fobj.write(str(i)+"\n\n")


class DoublyAddedError(Exception):
    pass


def main():
    students_lst=[]

    cred=int(input("Python course credits : "))
    strength=int(input("Python course capacity : "))
    python=PythonCourse(cred,strength,[])

    cred=int(input("Java course credits : "))
    strength=int(input("Java course capacity : "))
    java=JavaCourse(cred,strength,[])

    while(True):
        print("\n1 - Create Student")
        print("2 - Add Student to Special Course")
        print("3 - View Course Wise Student Details")
        print("4 - Write to text file")
        print("5 - Exit")

        choice=int(input("Enter your choice : "))

        if (choice==5):
            return

        elif (choice==1):
            n=int(input("Enter the number of students : "))
            for i in range(n):
                regno=int(input("Register number : "))

                duplicate=False
                for student in students_lst:
                    if (student.regno==regno):
                        duplicate=True

                if duplicate:
                    print("Register number already exists")
                    continue

                name=input("Name : ")
                sub1=int(input("Subject 1 marks : "))
                sub2=int(input("Subject 2 marks : "))
                sub3=int(input("Subject 3 marks : "))

                student=Student(regno,name,sub1,sub2,sub3)
                student.computeGrade()
                students_lst.append(student)
                print("Student created")

        elif (choice==2):
            regno=int(input("Register number : "))
            student=None

            for i in students_lst:
                if (i.regno==regno):
                    student=i
                    break

            if student is None:
                print("Student not found")
                continue

            try:
                if student in python.lst or student in java.lst:
                    raise DoublyAddedError("Student already added to a course")

                course=input("Choose Python or Java : ").lower()
                if (course=="python"):
                    selected=python
                elif (course=="java"):
                    selected=java
                else:
                    print("Invalid course")
                    continue

                if (len(selected.lst)>=selected.strength):
                    print("Course is full")
                else:
                    selected.lst.append(student)
                    print("Student added")

            except DoublyAddedError as e:
                print(e)

        elif (choice==3):
            python.display()
            java.display()

        elif (choice==4):
            # Clear once, then append details of both courses.
            with open("details.txt","w") as fobj:
                fobj.write("Course Wise Student Details\n")

            python.storeTextFile()
            java.storeTextFile()
            print("Details saved")

        else:
            print("Invalid choice")


if __name__=='__main__':
    main()

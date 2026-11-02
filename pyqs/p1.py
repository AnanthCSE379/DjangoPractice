class Questions:
    def __init__(self):
        self.QuestionBank = []

    def addQuestionset(self):
        domain = input("Domain: ")
        questions = []

        n = int(input("Number of questions: "))
        for i in range(n):
            question = input("Question: ")
            options = input("Options separated by commas: ").split(",")
            answer = input("Correct answer: ")
            questions.append([question, options, answer])

        self.QuestionBank.append({domain: questions})

    def createQuestions(self):
        n = int(input("Number of domain question sets: "))
        self.QuestionBank = []

        for i in range(n):
            self.addQuestionset()

        with open("Question_bank.txt", "w") as f:
            for QS in self.QuestionBank:
                for domain, questions in QS.items():
                    for question, options, answer in questions:
                        f.write(domain + "|" + question + "|" +
                                ",".join(options) + "|" + answer + "\n")

        print("Questions saved.")


class Quiz(Questions):
    def Quiz_Time(self):
        try:
            with open("Question_bank.txt", "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("Create questions first.")
            return

        domains = []
        for line in lines:
            domain = line.strip().split("|")[0]
            if domain not in domains:
                domains.append(domain)

        print("Available domains:", ", ".join(domains))
        domain = input("Choose domain: ")

        if domain not in domains:
            print("Invalid domain.")
            return

        name = input("Name: ")
        mobile = input("Mobile: ")
        correct = 0
        wrong = 0
        score = 0

        for line in lines:
            d, question, options, answer = line.strip().split("|")

            if d == domain:
                print("\n" + question)
                print("Options:", options)
                choice = input("Your answer: ").strip()

                if choice.lower() == answer.lower():
                    correct += 1
                    score += 1
                else:
                    wrong += 1
                    score -= 1

        total = correct + wrong
        print("\nTotal:", total)
        print("Correct:", correct)
        print("Wrong:", wrong)
        print("Score:", score)

        # Append each attempt as one ordinary text line.
        with open("Records.txt", "a") as f:
            f.write(name + "|" + mobile + "|" + domain + "|" +
                    str(total) + "|" + str(correct) + "|" +
                    str(wrong) + "|" + str(score) + "\n")

    def Topper(self):
        try:
            with open("Records.txt", "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("No records yet.")
            return

        totals = {}
        for line in lines:
            name, mobile, domain, total, correct, wrong, score = line.strip().split("|")
            key = (domain, mobile)

            if key not in totals:
                # Name, number of quizzes, combined score.
                totals[key] = [name, 0, 0]

            totals[key][1] += 1
            totals[key][2] += int(score)

        best = {}
        for key, data in totals.items():
            domain = key[0]

            if domain not in best:
                best[domain] = data
            elif data[1] > best[domain][1]:
                best[domain] = data
            elif data[1] == best[domain][1]:
                if data[2] > best[domain][2]:
                    best[domain] = data

        for domain, data in best.items():
            print("\nDomain:", domain)
            print("Topper:", data[0])
            print("Quizzes played:", data[1])
            print("Total score:", data[2])


app = Quiz()

while True:
    print("\n1. Create Questions")
    print("2. Play Quiz")
    print("3. Show Toppers")
    print("4. Exit")

    choice = input("Choice: ")

    if choice == "1":
        app.createQuestions()
    elif choice == "2":
        app.Quiz_Time()
    elif choice == "3":
        app.Topper()
    elif choice == "4":
        break
    else:
        print("Invalid choice.")

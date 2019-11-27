#File containing all classes
from functions import confirmation,match_input

class Question:
    def __init__(self,Question,Answer,checklist=None):
        self.Question = Question
        self.Answer = Answer
        self.check = checklist
        self.data = ""
        self.child = None
        self.answered = False

    def validity_check(self,user_input):
        if self.check:
            return match_input(user_input,self.check)
        else:
            return user_input

    def ask_question(self):
        user_input = input(self.Question+ "\n")
        self.data = self.validity_check(user_input)
        return user_input
    
    def check_answer(self):
        if self.Answer:
            if isinstance(self.data,list):
                if len(self.data)>1:
                    return self.Answer + " " + ", ".join(self.data[:-1]) + " and " + self.data[-1] + "?\n"
                elif len(self.data)==1:
                    return self.Answer + " " + str(self.data[0])+  "?\n"
            elif isinstance(self.data,str):
                return self.Answer + " " + self.data + "?\n"
        else: 
            return None

class Conversation:
    def __init__(self,title,questions):
        self.title = title
        self.questions = questions
        self.state = 0

    def ask_question(self):
        current_question = self.questions[self.state]
        f = open(self.title + ".txt","w")
        while not current_question.answered:
            user_input = current_question.ask_question()
            f.write(user_input)
            if current_question.Answer:
                user_input_confirm = input(self.questions[self.state].check_answer())
                f.write(user_input_confirm)
                if confirmation(user_input_confirm)==True:
                    current_question.answered = True
                else:
                    print("Sorry i didn't understand this, please tell me again")
            else:
                current_question.answered = True
        self.state += 1
        f.close()
    
    def hold_conversation(self,initial_state = 0):
        self.state = 0
        while self.state < len(self.questions):
            self.ask_question()
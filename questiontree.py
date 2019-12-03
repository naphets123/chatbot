#questiontree
from functions import *
import datetime


Totalquestions = []

Questions = [{"Title":"Name","Text":"Hello! What is your name?\n","control":get_Name},
                #{"Title""Text":"Do you own any trucks?\n","control":confirmation},
                {"Title":"NumTrucks","Text":"How many trucks do you own?\n","control":get_int},
                {"Title":"Brand","Text":"What brands are your trucks from\n","control":get_brands},
                {"Title":"NumBrand","Text":ask_number_brand,"control":get_int},
                {"Title":"Type","Text":ask_types,"control":get_types},
                {"Title":"NumType","Text":ask_number_type,"control":get_int},
                {"Title":"Engine","Text":ask_engine_size,"control":get_float},
                {"Title":"Axles","Text":ask_axles,"control":get_int},
                {"Title":"Weight","Text":ask_weight,"control":get_int},
                {"Title":"End","Text":"Thank your for your cooperation","control":None}
]

class Node:
    def __init__(self,state,Parent = None,AllAnswers={},filename = None,Question_list = None):
        self.state = state
        self.Questions = Question_list
        self.Children = []
        self.Parent = Parent
        self.Answer = None
        self.AllAnswers = AllAnswers
        self.filename = filename
        self.current_question = self.Questions[state]

    def create_children(self):
        if self.Answer:
            if isinstance(self.Answer,list):
                for i in range(len(self.Answer)):
                    child_answerlist = dict(self.AllAnswers)
                    child_answerlist.update({self.current_question["Title"]:self.Answer[i]})
                    Child = Node(self.state + 1,self,child_answerlist,filename=self.filename,Question_list=self.Questions)
                    self.Children.append(Child)
                    Totalquestions.append(Child)
            else:
                child_answerlist = dict(self.AllAnswers)
                child_answerlist.update({self.current_question["Title"]:self.Answer})
                Child = Node(self.state + 1,self,child_answerlist,filename = self.filename,Question_list=self.Questions)
                self.Children.append(Child)
                Totalquestions.append(Child)

    def ask_user_input(self,string):
        self.save(string)
        user_input = input(string)
        self.save(user_input)
        return user_input

    def save(self,string):
        f = open(self.filename,"a")
        f.write(string)
        f.close()

    def ask_confirm(self,value):
        user_input = self.ask_user_input("Is this answer correct? " + stringify(value) + "\n")
        if confirmation(user_input):
            return True
        else:
            return False
        
    def ask(self):
            if callable(self.current_question["Text"]):
                question_string = self.current_question["Text"](self)
            else:
                question_string = self.current_question["Text"]
            user_input = self.ask_user_input(question_string)
            valid_info = input_check(user_input,self,self.current_question["control"])
            if valid_info not in [None,[]]:
                #self.ask_confirm(valid_info):
                self.Answer = valid_info
                state = True                    
            else:
                Error_msg = "Sorry I could not understand your answer please try again"
                self.save(Error_msg)
                state = False
            return state

    def conversation(self):
        if self.current_question["Title"] == "End":
            self.ask()
            return True
        if not self.Answer:
                answered = False
                while answered == False:
                    answered = self.ask()
                self.create_children()
                return False
        else:
            for i in range(len(self.Children)):
                checked = self.Children[i].conversation()
                if checked:
                    return True
            return False



a = Node(0,filename="Conversation.txt",Question_list=Questions)
finished = False
while not finished:
    finished = a.conversation()

"""
for i in Totalquestions:
    print(i.AllAnswers)
"""




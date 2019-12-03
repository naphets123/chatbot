#questiontree
from functions import *
import datetime



Questions = [{"Title":"Name","Text":"Hello! What is your name?\n","control":get_Name},
            {"Title":"CompanyName","Text":"What is the name of your company?\n","control":get_Name},
            {"Title":"NumTrucks","Text":"How many trucks do you own?\n","control":get_int},
            {"Title":"Brand","Text":"What brands are your trucks from\n","control":get_brands},
            {"Title":"NumBrand","Text":ask_number_brand,"control":get_int},
            {"Title":"Type","Text":ask_types,"control":get_types},
            {"Title":"NumType","Text":ask_number_type,"control":get_int},
            {"Title":"Engine","Text":ask_engine_size,"control":get_float},
            {"Title":"Axles","Text":ask_axles,"control":get_int},
            {"Title":"Weight","Text":ask_weight,"control":get_int},
            {"Title":"Load","Text":ask_load,"control":get_int},
            {"Title":"End","Text":"Thank your for answering all question\n Have a nice day!","control":None}
]

class Tree:
    def __init__(self,Question,filename,Nodes=[]):
        self.filename = filename
        self.Questions = Questions
        self.Nodes = Nodes
    
    #Provisorial Ouput of data
    def print_full_branches(self):
        for n in self.Nodes:
            if Questions[-2]["Title"] in n.AllAnswers.keys():
                print(n.AllAnswers)

class Node:
    def __init__(self,state,Parent = None,AllAnswers={},Tree=None):
        self.state = state
        self.Children = []
        self.Tree = Tree
        self.Answer = None
        self.Parent = Parent
        self.AllAnswers = AllAnswers
        self.current_question = self.Tree.Questions[state]

    def create_children(self):
        if self.Answer:
            if isinstance(self.Answer,list):
                for i in range(len(self.Answer)):
                    child_answerlist = dict(self.AllAnswers)
                    child_answerlist.update({self.current_question["Title"]:self.Answer[i]})
                    Child = Node(self.state + 1,self,child_answerlist,self.Tree)
                    self.Children.append(Child)
                    self.Tree.Nodes.append(Child)
            else:
                child_answerlist = dict(self.AllAnswers)
                child_answerlist.update({self.current_question["Title"]:self.Answer})
                Child = Node(self.state + 1,self,child_answerlist,self.Tree)
                self.Children.append(Child)
                self.Tree.Nodes.append(Child)

                #### This is not really part of the tree but we want to track all nodes in this

    def ask_user_input(self,string):
        self.save(string)
        user_input = input(string)
        self.save(user_input)
        return user_input

    def save(self,string):
        f = open(self.Tree.filename,"a")
        f.write(string + "\n")
        f.close()

    def back(self,string):
        #If user made a mistake, let him roll back to the last question
        if cancel(string,self):
            ask_cancel = "Do you want to go back to the last question?\n"
            user_input = self.ask_user_input(ask_cancel)
            self.save(ask_cancel)
            self.save(user_input)
            if confirmation(user_input,self) and self.state != 0:
                Parent = self.Parent
                Parent.Children = []
                Parent.Answer = None
                Parent.current_question = Parent.Tree.Questions[Parent.state]
                return True
        else:
            return False
            

    def ask(self):
            #Get appropriate Question and ask the user
            if callable(self.current_question["Text"]):
                question_string = self.current_question["Text"](self)
            else:
                question_string = self.current_question["Text"]
            user_input = self.ask_user_input(question_string)

            #Check the user input for Error, first if he complains, then if his input is an valid answer
            check = self.back(user_input)
            if check:
                self.Parent.conversation()
                return True
            valid_info = input_check(user_input,self,self.current_question["control"])
            if valid_info not in [None,[]]:
                self.Answer = valid_info
                return True                
            else:
                Error_msg = "Sorry I could not understand your answer please try again"
                self.save(Error_msg)
                return False

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







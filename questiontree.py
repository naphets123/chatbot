#questiontree
from functions import *
import datetime


class Tree:
    def __init__(self,Questions,filename,Nodes=[]):
        self.filename = filename
        self.Questions = Questions
        self.Nodes = Nodes
    
    #Provisorial Ouput of data
    def print_full_branches(self):
        for n in self.Nodes:
            if self.Questions[-2]["Title"] in n.AllAnswers.keys():
                print(n.AllAnswers)

class Node:
    def __init__(self,state,Parent = None,AllAnswers={},Tree=None,Total=[0,0]):
        self.state = state
        self.Children = []
        self.Tree = Tree
        self.Total = Total
        self.Answer = None
        self.Parent = Parent
        self.AllAnswers = AllAnswers
        self.current_question = self.Tree.Questions[state]

    def create_children(self):
        if self.Answer:
            if isinstance(self.Answer,list):
                for i in range(len(self.Answer)):
                    self.create_single_child(self.Answer[i],[1,1])
                    self.Total[1]-=1
            else:
                self.create_single_child(self.Answer,self.Total)
 

    def create_single_child(self,answer,Total):
        child_answerlist = dict(self.AllAnswers)
        child_answerlist.update({self.current_question["Title"]:answer})
        Child = Node(self.state + 1,self,child_answerlist,self.Tree,Total)
        self.Children.append(Child)
        self.Tree.Nodes.append(Child)

    def ask_user_input(self,string):
        self.save(string)
        user_input = input(string)
        self.save(user_input)
        return user_input
    
    def msg_user(self,string):
        self.save(string)
        print(string)

    def save(self,string):
        f = open(self.Tree.filename,"a")
        f.write(string + "\n")
        f.close()

    
    def drain_amount(self,amount):
        if self.Parent == None or self.Parent.Total==[0,0]:
            change = int(amount)
            self.Total[0]=change
            self.Total[1]=change
        elif isinstance(self.Parent.Answer,list):
            change = int(amount)-1
            #check with change-1 due to assignment of 1 at creation of child
            if self.Parent.Total[1]>=(change):
                self.Total[0]+=change
                self.Total[1]+=change
                self.Parent.Total[1]-=change
            else:
                self.msg_user("Error, invalid number")
        else: 
            self.msg_user("Error")

    def get_question(self):
        if callable(self.current_question["Text"]):
                question_string = self.current_question["Text"](self)
        else:
            question_string = self.current_question["Text"]
        return question_string


    def roll_back(self):
        #If user made a mistake, let him roll back to the last question
        Parent = self.Parent
        Parent.Children = []
        Parent.Answer = None
        Parent.current_question = Parent.Tree.Questions[Parent.state]
        Parent.Total[1]=Parent.Total[0]
    

    def input_check(self,user_input,Node,check_option):
        #Check if there is negation in the users answer
        if cancel(user_input,self):
            user_input = self.ask_user_input("Do you want to go back to the last question?\n")
            if confirmation(user_input,self) and self.Parent != None:
                self.roll_back()
                return True, user_input, " "
        #Otherwise if there is a function for checking the input
        elif check_option:
            checked_value = check_option(user_input,Node)
            if checked_value in [None,[]]:
                return False, checked_value, "Sorry could not understand your answer"
            elif self.current_question["control"] == get_amount and self.Parent is not None:
                if 1 <= int(checked_value) <= self.Parent.Total[1]+1:
                    return True, checked_value, ""
                else:
                    return False, checked_value, "Sorry but this number is invalid, biggest possible number is " + str(self.Parent.Total[1]+1)
            else:
                return True, checked_value, " "
        else:
            return True, user_input, " "


    def ask(self):
        #Get appropriate Question and ask the user
        question_string = self.get_question()
        user_input = self.ask_user_input(question_string)
        #Check the user input for Error, first if he complains, then if his input is an valid answer
        checked,valid_info,error_msg = self.input_check(user_input,self,self.current_question["control"])
        if checked :
            self.msg_user("Answer that was understood: " + stringify(valid_info))
            self.Answer = valid_info
            if self.current_question["control"] == get_amount:
                self.drain_amount(self.Answer)
            return True
        else:
            self.msg_user(error_msg)
            return False

    def conversation(self):
        if self.current_question["Title"] == "End":
            self.ask()
            return True
        if not self.Answer:
                answered = False
                while not answered:
                    answered = self.ask()
                self.create_children()
                return False
        else:
            initial_list = self.Children
            for i in range(len(self.Children)):
                if self.Children != initial_list:
                    break
                checked = self.Children[i].conversation()
                
                if checked:
                    return True
            return False







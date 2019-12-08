#questiontree
from functions import *
import datetime


class Tree:
    def __init__(self,Questions,filename,Nodes=[]):
        self.filename = filename
        self.Questions = Questions
        self.Nodes = Nodes
    
    def initiate(self):
        root = Node(0,None,Tree=self)
        self.Nodes.append(root)
        finished = False
        while not finished:
            finished = root.conversation()

    #Provisorial Ouput of data
    def print_full_branches(self):
        for n in self.Nodes:
            if self.Questions[-2]["Title"] in n.AllAnswers.keys():
                print(n.AllAnswers)
    
    def get_last_question(self):
        last_asked = False
        count = 1
        while not last_asked:
            last = self.Nodes[-count]
            last_asked=last.asked
            count+=1
        return last


class Node:
    def __init__(self,state,Parent = None,AllAnswers={},Tree=None,Total=[0,0],asked = None):
        self.state = state
        self.Children = []
        self.Tree = Tree
        self.Total = Total
        self.asked = asked
        self.Answer = None
        self.Parent = Parent
        self.AllAnswers = AllAnswers
        self.current_question = self.Tree.Questions[state]

    def is_branching(self):
        if not isinstance(self.Answer,list):
            return False
        else:
            if len(self.Answer) in [0,1]:
                return False
            else:
                return True

    def siblings_answered(self):
        siblings = self.Parent.Children
        counter = 0
        for i in siblings:
            if i.Answer is None:
                counter+=1
        if counter ==1:
            return True
        else:
            return False

    def create_children(self):
        if self.Answer:
            branch = self.is_branching()
            if branch:
                for i in range(len(self.Answer)):
                    self.create_single_child(self.Answer[i],[1,1])
                    self.Total[1]-=1
            else:
                self.create_single_child(self.Answer,[0,0])
 

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
        print(string + "\n")

    def save(self,string):
        f = open(self.Tree.filename,"a")
        f.write(string + "\n")
        f.close()

    def drain(self):
        if self.Parent is not None:
            if self.current_question["input"]==get_amount:
                amount = int(self.Answer)
                if self.Parent.is_branching():
                        change = amount-1
                        if self.Parent.Total[1]>=(change):
                            self.Total[0]+=change
                            self.Total[1]+=change
                            self.Parent.Total[1]-=change
                elif self.Parent.Total == [0,0]:
                    self.Total[0]=amount
                    self.Total[1]=amount
                else:
                    self.Total[0]+=self.Parent.Total[1]
                    self.Total[1]+=self.Parent.Total[1]
                    self.Parent.Total[1]-=self.Total[1]
            else:
                #If we are not in a assigning totals, we just pass the identical totals to the next question
                    self.Total[0]+=self.Parent.Total[1]
                    self.Total[1]+=self.Parent.Total[1]
                    self.Parent.Total[1]-=self.Total[1]


    def roll_back(self):
        #This function does the inverse to self.drain()
        if len(self.Children)>1:
            self.Total[1]+=len(self.Children)
        self.Children = []
        self.Answer = None
        if self.Parent is not None and self.Parent.Total != [0,0]:
            if self.Parent.is_branching():
                self.Parent.Total[1]+=self.Total[1]-1
                self.Total[0] = 1
                self.Total[1] = 1
            else:
                self.Parent.Total[1]+=self.Total[0]
                self.Total[0] = 0
                self.Total[1] = self.Total[0]

    def get_question(self):
        if callable(self.current_question["Text"]):
                question_string = self.current_question["Text"](self)
        else:
            question_string = self.current_question["Text"]
        return question_string



    def ask(self):
        #Check if answer to this question is already given by context and previous answers and skip asking
        answered, answer = answer_clear(self)
        if answered:
            self.Answer = answer
            self.asked = False
            self.drain()
            return True
        #Get appropriate Question and ask the user
        question_string = self.get_question()
        user_input = self.ask_user_input(question_string)
        #Check if user wants to correct himself
        if back_to_last_answer(user_input,self):
            return True
        #process the answer and check if it is valid
        checked,valid_info,error_msg = input_value_check(user_input,self)
        if checked :
            self.msg_user("Answer that was understood: " + stringify(valid_info))
            self.Answer = valid_info
            self.asked = True
            self.drain()
            return True
        else:
            self.msg_user(error_msg)
            return False

    def conversation(self):
        #This function is called to run the chatbot and recursively creates the Tree of questions
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







from language import *

def back_to_last_answer(user_input,Node):
    if cancel(user_input,Node):
        user_input = Node.ask_user_input("Do you want to go back to the last question?\n")
        if confirmation(user_input,Node) and Node.Parent is not None:
            last_asked = False
            last = Node
            while True:

                last = Node.Tree.Nodes.pop()
                last.roll_back()
                last_asked=last.asked
                if last_asked or Node.Tree.Nodes == []:
                    break
            last.asked = None
            last.conversation()
            return True
        else:
             return False
    else:
        return False


def answer_clear(Node):
    #Currently this check will only happen
    Parent = Node.Parent
    if Parent is not None and Node.current_question["input"]==get_amount:
        check_branch = Parent.is_branching()
        check_total = Parent.Total[1]==0
        if check_branch and check_total:
            return True, 1
        elif Node.siblings_answered() and check_branch:
            #if there is only a single option left give it all the remaining trucks
            return True, Node.Parent.Total[1]+1
        elif not check_branch and Parent.Total[0] != 0:
            Node.Total[0]=Node.Parent.Total[1]
            Node.Total[1]=Node.Total[0]
            return True, Node.Parent.Total[1]
        else:
            return False, None
    else:
        return False, None

def input_value_check(user_input,Node):
    #Otherwise if there is a function for checking the input
    get_value = Node.current_question["input"]
    check_option = Node.current_question["control"]
    received_value = get_value(user_input,Node)
    if received_value is None or  received_value == []:
        return False, received_value, "Sorry, I could not understand your answer"
    else:
        if check_option is not None:
            return check_option(received_value,Node)
        else:
            return True, received_value,""

def valid_options(answer,Node):
        if isinstance(answer,list):
            answerlength = len(answer)
        else:
            answerlength = 1
        if answerlength>Node.Parent.Total[0]:
            return False,answer, "Invalid number of options chosen, maximum possible number is " + str(Node.Parent.Total[0])
        else:
            return True,answer,""

def valid_amount(amount,Node):
    if Node.Parent is not None and Node.Parent.Total[0] is not 0:
        if 1 <= int(amount) <= Node.Parent.Total[1]+1:
            return True,str(amount),""
        else:
            return False,str(amount),"Invalid value. It shoulb be between 1 and " + str(Node.Parent.Total[1]+1)
    else:
        return True,amount,""


    











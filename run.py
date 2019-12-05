#file to run the chatbot
from questiontree import Tree,Node
from functions import *
#from functions import match_input, confirmation


Questions = [#{"Title":"Name","Text":"Hello! What is your name?\n","control":get_Name},
            #{"Title":"CompanyName","Text":"What is the name of your company?\n","control":get_Name},
            #{"Title":"AnyTruck","Text":"Do you own any trucks?\n","control":confirmation},
            {"Title":"NumTrucks","Text":"How many trucks do you own?\n","control":get_amount},
            {"Title":"Brand","Text":"What brands are your trucks from\n","control":get_brands},
            {"Title":"NumBrand","Text":ask_number_brand,"control":get_amount},
            {"Title":"Type","Text":ask_types,"control":get_types},
            {"Title":"NumType","Text":ask_number_type,"control":get_amount},
            {"Title":"Engine","Text":ask_engine_size,"control":get_float},
            {"Title":"Axles","Text":ask_axles,"control":get_int},
            {"Title":"Weight","Text":ask_weight,"control":get_int},
            {"Title":"Load","Text":ask_load,"control":get_int},
            {"Title":"End","Text":"Thank your for answering all question\n Have a nice day!","control":None}
]

Chat = Tree(Questions,"Conversation.txt",[])
a = Node(0,Tree = Chat)
finished = False
while not finished:
    finished = a.conversation()

Chat.print_full_branches()
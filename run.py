#file to run the chatbot
from questiontree import Tree,Node
from functions import *
from language import *
#from functions import match_input, confirmation


Questions = [{"Title":"Name","Text":"Hello! What is your name?\n","input":get_Name,"control":None},
            {"Title":"CompanyName","Text":"What is the name of your company?\n","input":get_Name,"control":None},
            {"Title":"NumTrucks","Text":"How many trucks do you own?\n","input":get_amount,"control":valid_amount},
            {"Title":"Brand","Text":"What brands are your trucks from\n","input":get_brands,"control":valid_options},
            {"Title":"NumBrand","Text":ask_number_brand,"input":get_amount,"control":valid_amount},
            {"Title":"Type","Text":ask_types,"input":get_types,"control":valid_options},
            {"Title":"NumType","Text":ask_number_type,"input":get_amount,"control":valid_amount},
            {"Title":"Engine","Text":ask_engine_size,"input":get_float,"control":None},
            {"Title":"Axles","Text":ask_axles,"input":get_int,"control":None},
            {"Title":"Weight","Text":ask_weight,"input":get_int,"control":None},
            {"Title":"Load","Text":ask_load,"input":get_int,"control":None},
            {"Title":"End","Text":"Thank your for answering all question\n Have a nice day!","input":get_nothing,"control":None}
]

Chat = Tree(Questions,"Conversation.txt",[])
Chat.initiate()

Chat.print_full_branches()
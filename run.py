#file to run the chatbot
from classes import Question, Conversation
#from functions import match_input, confirmation
import spacy
import datetime
from functions import get_number

Name = Question("What is your name?","Your name is")
Trucks = Question("Do you own any trucks?",None)
Number = Question("How many trucks do you own?","You own ",{"function":get_number})
Brands = Question("What brands are your trucks?", "So the brands are",{"wordlist":["Scania","MAN","Volvo","Mercedes"]})
Types = Question("What are the models of your trucks?", "So the types are", {"wordlist":["XLR-2000", "X-wing", "Millenium-falcon"]})
Axes = Question("How many axes do they have?","They have ",{"function":get_number})
Capacity = Question("What is their capacity","They have a capacity of ",{"function":get_number})
Ending = Question("Thank you registering your fleet! After you confirm this dialogue will close.Have a nice day!",None)
a = Conversation(str(datetime.datetime.now()),[Number,Brands,Types,Axes,Capacity,Ending])
a.hold_conversation()
# Simple Chatbot to receive truck-specifications
___
The chatbot starts by executing run.py
___
Dependencies
All language modeling is done with the spacy library, nltk is exclusively used for the Levensthein-distance.  
The list of truck-manufacturers and models is taken from https://en.wikipedia.org/wiki/List_of_trucks  
Apart from the libraries in the dependenc folder, you also have to load the language model for spacy with  
python -m spacy download en_core_web_sm
___
Todo:  
-Track totals and prevent incoherent numbers  
-Replace truck models and Brands with a more cohesive list  
-Implement more checks to give reasonable input ranges  

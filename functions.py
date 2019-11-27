import spacy
from spacy.matcher import Matcher
import nltk 
from nltk.metrics import edit_distance

nlp = spacy.load("en_core_web_sm")


def phrase_checker(phrase,pattern_list):
    matcher = Matcher(nlp.vocab)
    negatives = False
    matcher.add("Confirmation", None, pattern_list)
    doc = nlp(phrase)
    matches = matcher(doc)
    return matches

def confirmation(phrase):
    #Function to check if user confirms last statement
    matches = phrase_checker(phrase,[{"LOWER": "yes"}],[{"LOWER": "correct"}],[{"LOWER": "right"}],[{"LOWER": "true"}])
    negatives = False
    for token in doc:
        if token.dep_ == "neg":
            negatives = True
    if len(matches) > 0 and not negatives:
        return True
    else:
        return False

    
def back(phrase):
    matches = phrase_checker([{"LOWER": "stop"}],[{"LOWER": "back"}],[{"LOWER": "return"}],[{"LOWER": "mistake"}])


def match_input(input_text,expected_input):
    text_spacy = nlp(input_text)
    text_matches = []
    keys = expected_input.keys()
    if "wordlist" in keys:
        for token in text_spacy:
            for text in expected_input["wordlist"]:
                distance = edit_distance(text.lower(),token.text.lower())
                if (distance < 2):
                    text_matches.append(text.lower())
    if "function" in keys:
        text_matches =  expected_input["function"](input_text)
    return text_matches

def get_number(user_input):
    input_doc = nlp(user_input)
    numbers = []
    for token in input_doc:
        if token.pos_ == "NUM":
            numbers.append(token.text)
    return numbers

def find_word(wordtype):
    nlp = spacy.load("en_core_web_sm")
    
"""
nlp = spacy.load("en_core_web_sm")
doc = nlp("This kind of not text")

for token in doc:
    print(token.text, token.pos_, token.dep_)

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
"""
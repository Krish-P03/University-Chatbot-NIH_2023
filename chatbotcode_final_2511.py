# -*- coding: utf-8 -*-
"""chatbotcode_final_2511.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Dv06xf-wdVfz3zoYWZcnx0FiBYGXPji
"""

import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
from nltk.tokenize import sent_tokenize
import json
import tensorflow as tf
import random
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('popular')

lemmatizer = WordNetLemmatizer()

model = load_model('finalmodel.h5')
intents = json.loads(open('Final_2511.json').read())
words = pickle.load(open('final_texts.pkl', 'rb'))
classes = pickle.load(open('final_labels.pkl', 'rb'))

lemmatizer = WordNetLemmatizer()
wrds = []
ignore_letters = ['?', '!']
wrds = [lemmatizer.lemmatize(w) for w in wrds if w not in ignore_letters]
wrds = sorted(set(wrds))
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))

def predict_class(sentence,model):


    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):

    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            responses = i['responses']
            response = random.choice(responses)
            sentences = sent_tokenize(response)
            sentence = random.choice(sentences)
            break
    return sentence

print("Start")
print("Chatbot Response: Hello! How can I assist you today?")
while True:
    message = input("You: ")
    if message.lower() == 'exit':
        print("Chatbot Response: Have a nice day!")
        break

    ints = predict_class(message, model)
    res = get_response(ints, intents)
    print("Chatbot Response:", res)


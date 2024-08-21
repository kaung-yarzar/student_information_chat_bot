import warnings
warnings.filterwarnings('ignore')
import nltk
import string
import streamlit as st
import random
import time

from nltk.stem import WordNetLemmatizer


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pymongo import MongoClient

from connect_db import connect_training_data_collection
collection = connect_training_data_collection()



nltk.download('wordnet')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


# client = MongoClient('mongodb://admin:admin12345@cluster0-shard-00-00.g1sch.mongodb.net:27017,cluster0-shard-00-01.g1sch.mongodb.net:27017,cluster0-shard-00-02.g1sch.mongodb.net:27017/?ssl=true&replicaSet=atlas-i75tpn-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
# db = client['tumltaproject']
# collection = db['training_data']


data = collection.find()
sentences = ""
for doc in data:
    text_value = doc.get("text", "")
    sentences += text_value + "\n"

#client.close()

sen = nltk.sent_tokenize(sentences) # make sentences
words = nltk.word_tokenize(sentences) # make words


wnlem = nltk.stem.WordNetLemmatizer()
def perfom_lemmatization(tokens):
  return[wnlem.lemmatize(token) for token in tokens]

pr = dict((ord(punctuation),None) for punctuation in string.punctuation)


# To process data
def get_processed_text(document):
  return perfom_lemmatization(nltk.wordpunct_tokenize(document.lower().translate(pr)))


# def generate_greeting_responses(greeting):
#   for token in greeting.split():
#     if token.lower() in greeting_inputs:
#       return random.choice(greeting_responses)
    
    
def generate_response(user_input):
  bot_response = ''
  sen.append(user_input)

  word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
  word_vectors = word_vectorizer.fit_transform(sen)
  similar_vector_values = cosine_similarity(word_vectors[-1], word_vectors)
  similar_sentence_number = similar_vector_values.argsort()[0][-2]


  match_vector = similar_vector_values.flatten()
  match_vector.sort()
  vector_matched = match_vector[-2]


  if vector_matched == 0:
    bot_response = bot_response + 'I apologize, I’m having trouble comprehending your question'
    return bot_response

  else:
    if '?' in sen[similar_sentence_number]:
      bot_response = bot_response + sen[similar_sentence_number + 1]

    else:
      bot_response = bot_response + sen[similar_sentence_number]

    return bot_response



def response_delay(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.12)

import re

def chatbot():
  st.title('Student Information Chatbot')
  
  # Initialize chat history
  # if "messages" not in st.session_state:
  #     st.session_state.messages = []


  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
      with st.chat_message(message["role"], avatar= message["avatar"]):
          st.markdown(message["content"])


  # React to user input
  if prompt := st.chat_input("What can I assist you?"):
      
      with st.chat_message("user", avatar="🧑‍💻"):
         st.markdown("Hello Wecome from TU Meiktila Student Information Chatbot. You can ask me questions about TU Meiktila...")

      # Display user message in chat message container
      with st.chat_message("user", avatar="🧑‍💻"):
          st.markdown(prompt)

      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": prompt, "avatar" : "🧑‍💻"}) 


  if prompt != None:
    response = f"{generate_response(prompt)}"
    
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🤖"):
        if 'https' in response:
          response = response[:-1]
          st.image(response)
          
        else:   
          st.write_stream(response_delay(response))

        sen.remove(prompt)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar" : "🤖"})



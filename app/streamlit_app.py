import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from lime.lime_text import LimeTextExplainer
import os

st.set_page_config(
    page_title='Flysafe Analytics', 
    page_icon= "https://w7.pngwing.com/pngs/503/7/png-transparent-airplane-logo-flight-attendant-air-travel-airplane-aviation-avion-text-logo-flight.png", 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items=None
    )

with st.sidebar:
    """
    # About Us:
    ----
    ## Stay Protected When Travel

    When you plan a trip to abroad, hotel bookings, sight-seeing & shopping are the things you usually plan precisely but buying a Travel Insurance is seldom thought. Very few people plan for unforeseen events like flight delays, personal accidents, even a hospital stay in a strange unknown place.
    """
path = "/home/appuser/app/"
#path = "E:/Major_Project/app/"
with open(path + 'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True) 

st.image("https://flysafe.in/images/logo-white.svg", width=200)
st.header('FlySafe Analytics Sentiment Analysis Dashboard')


def load_model_vectorizer(path):
    with open(path + "Models/my_classifier.pickle", 'rb') as f:
        model = pickle.load(f)
    with open(path + "Models/tfidf_vectorizer.pkl", 'rb') as ft:
        tfidf = pickle.load(ft)
    #tfidf = TfidfVectorizer(ngram_range=(1, 3),max_features=2000)
    #df = pd.read_excel(path+'preprocessed.xlsx')
    #data = df['clean_comment'].fillna('')
    return model, tfidf


def make_prediction(model,tfidf,data):
    vectorized = tfidf.transform(data)
    result = model.predict(vectorized)
    if result[0] == 1:
        prediction = 'Positive'
    else:
        prediction = 'Negative'
    st.write("""Prediction: """, prediction)

def Explainer(text,tfidf,model):
    explainer = LimeTextExplainer(class_names = ['Negative','Positive'])
    pipe = make_pipeline(tfidf, model)
    exp = explainer.explain_instance(text, pipe.predict_proba, num_features = 10)
    return exp


   

live_text = st.text_area(label='',placeholder='Enter your reivew:')
button = st.button('Predict Sentiment:')
model, tfidf = load_model_vectorizer(path)
data = np.array([live_text])

if button:
    make_prediction(model,tfidf,data)
    with st.spinner('Analysing...'):
        components.html(
            Explainer(live_text,tfidf,model).as_html(), 
            height=300,
            scrolling=False
            )
                    

    



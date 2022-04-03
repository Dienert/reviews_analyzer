from cProfile import label
from email.utils import parsedate
from turtle import position
import streamlit as st
import pandas as pd
from math import floor
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk import tokenize

import streamlit as st
import time
import numpy as np

# can only set this once, first thing to set
st.set_page_config()

visualizations = ["Wordcloud", "Top 10 words", "Positive versus Negative", "Timeline", "Animation"]
sentiments = ["Positive", "Negative"]
preprocessing = ["Before Preprocessing", "After Preprocessing"]
models = ["Random Forest with Bag-of-words", "CNN", "LSTM", "Bert"]

# Top text area
with st.container():
    # st.title("Sentiment Analisys")
    st.title("Reviews for the book \"Outliers: The Story of Success\"")

column_1, column_2, column_3 = st.columns(3)
with column_1:
    visualization_chosen = st.selectbox("Visualization", visualizations, 0)
with column_2:
    preprocessing_chosen = st.selectbox("Preprocessing", preprocessing, 0)
with column_3:
    model_chosen = st.selectbox("Choose the model", models, 0)

# Get data before preprocessing
@st.cache()
def load_dataset_before_preprocessing():
    path = f'../dataset/graphs/df_concat_initial.csv'
    return pd.read_csv(path)

# Get data after preprocessing 1
@st.cache()
def load_dataset_after_preprocessing():
    path = f'../dataset/graphs/concat_after_processing.csv'
    df = pd.read_csv(path)
    df = df.dropna(subset=['processing5'])
    return df

# Get data with date
@st.cache()
def load_dataset_with_date():
    path = f'../dataset/joined/reviews-outliers-the_story_of_success_processed.csv'
    df = pd.read_csv(path)
    df = df.dropna(subset=['date'])
    return df

sentiment_chosen = None
if visualization_chosen == 'Wordcloud' or visualization_chosen == "Top 10 words":
    sentiment_chosen = st.selectbox("Sentiment", sentiments, 0)

    if preprocessing_chosen == 'After Preprocessing':
        df = load_dataset_after_preprocessing().copy()
    elif preprocessing_chosen == 'Before Preprocessing':
        df = load_dataset_before_preprocessing().copy()

elif visualization_chosen == 'Timeline':
    df = load_dataset_with_date().copy()
else:
    df = load_dataset_after_preprocessing().copy()


def pie_plot_sentiment(text):
    
    counts = text.y.value_counts()
    total_negatives = counts[0]
    total_positives = counts[1]
    
    labels = 'Positives', 'Negatives'
    sizes = [total_negatives, total_positives]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    
    plt.figure(figsize=(10,7))
    plt.axis('off')
    plt.show()
    st.pyplot(fig, use_container_width=True)
    return fig

def plot_bar_graph_reviews_per_year(df):

    df.index = pd.to_datetime(df['date'], format='%Y-%m-%d')

    figure = plt.figure(figsize=(12,8))

    negatives_per_year = df[df['stars'] == 0]
    
    res = pd.DataFrame([])
    res['negatives'] = negatives_per_year.groupby([negatives_per_year.index.year])['stars'].count()
    print(res['negatives'])

    positives_per_year = df[df['stars'] == 1]
    res['positives'] = positives_per_year.groupby([positives_per_year.index.year])['stars'].count()
    print(res['positives'])
    
    ax = sns.lineplot(x = res.index, y = res['negatives'], color ='red', label='Negative')
    ax.set_title("Sentiments through time")
    ax.set_xlabel("Years")
    ax.set_ylabel("Number of Reviews")

    sns.lineplot(ax=ax, x = res.index, y = res['positives'], color ='green', label='Positive')

    plt.show()
    st.pyplot(figure, use_container_width=True)
    return figure

def plot_animation(df):
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    new_reviews = [100, 80, 45, 32, 56, 23]
    old_reviews = new_reviews

    # df.index = pd.to_datetime(df['date'], format='%Y-%m-%d')

    chart = st.line_chart(old_reviews)
    
    for i in range(1, 10):
        status_text.text("%i%% Complete" % i)

        new_reviews = [x + 3 for x in new_reviews]
        chart.add_rows(new_reviews)
        progress_bar.progress(i)
        old_reviews = new_reviews
        
        time.sleep(0.05)

    progress_bar.empty()

    st.button("Re-run")

def generate_wordcloud_sentiment(text, target, sentiment):
    
    sentiment_text = text.query("y == " f'{sentiment}')

    all_words = ' '.join([text for text in sentiment_text[target]])

    wordCloud = WordCloud(width=400, height=250,
                            max_font_size=110).generate(all_words)

    figure = plt.figure(figsize=(10,7))
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot(figure, use_container_width=True)
    return figure

def pltplot_high_frequence_words(dataset, review_col, sentiment, number_of_words):
    # nltk.download("all")
    sentiment_text = dataset.query("y == " f'{sentiment}')
    all_words = ' '.join([dataset for dataset in sentiment_text[review_col]])
    print(len(all_words))
    token_space = tokenize.WhitespaceTokenizer()
    tokens_corpus = token_space.tokenize(all_words)
    frequence = nltk.FreqDist(tokens_corpus)

    tokens_corpus = token_space.tokenize(all_words)
    frequence = nltk.FreqDist(tokens_corpus)
    df_frequence = pd.DataFrame({"Word": list(frequence.keys()),
                             "Frequence": list(frequence.values())})

    df_frequence_largest = df_frequence.nlargest(columns = "Frequence", n = number_of_words)

    figure = plt.figure(figsize=(12,8))
    ax = sns.barplot(data = df_frequence_largest, x = "Word", y = "Frequence", color ='orange')
    ax.set(ylabel = "Counting")
    plt.show()
    st.pyplot(figure, use_container_width=True)
    return figure

sentiments = {'Positive': 1,
              'Negative': 0}
column = 'x'
if preprocessing == "After Preprocessing":
    column = 'processing5'
elif preprocessing == "Before Preprocessing":
    column = 'x'

print(f"Visualization: {visualization_chosen}")
print(f"Preprocesssing: {preprocessing_chosen}")
print(f"Model: {model_chosen}")
print(f"Sentiment: {sentiment_chosen}")

if visualization_chosen == "Timeline":
    plot_bar_graph_reviews_per_year(df)
elif visualization_chosen == "Positive versus Negative":
    pie_plot_sentiment(df)
elif visualization_chosen == "Wordcloud":
    generate_wordcloud_sentiment(df, column, sentiments[sentiment_chosen])
elif visualization_chosen == "Top 10 words":
    pltplot_high_frequence_words(df, column, sentiments[sentiment_chosen], 10)
elif visualization_chosen == "Animation":
    plot_animation(df)
else:
    generate_wordcloud_sentiment(df, column, sentiments[sentiment_chosen])
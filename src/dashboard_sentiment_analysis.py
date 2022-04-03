from cProfile import label
from email.utils import parsedate
from turtle import position
import streamlit as st
import pandas as pd
import numpy as np
from math import floor
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import leafmap.foliumap as leafmap
import nltk
from nltk import tokenize
from datetime import datetime

import streamlit as st
import time
import numpy as np

# can only set this once, first thing to set
st.set_page_config()

type_of_visualization = {
    "Wordcloud before preprocessing": {"type": 'wordCloud_before'},
    "Worcloud after preprocessing": {"type": 'wordCloud_after'},
    "Top 10 words before preprocessing": {"type": "barplot_before"},
    "Top 10 words after preprocessing": {"type": "barplot_after"},
    "Positive versus Negative": {"type": "pie_plot"},
    "Line chart": {"type":"line_chart"}
}

visualizations = type_of_visualization.keys()

types_of_sentiments = {"Positive": {"sentiment": 'positive'}, 
                    "Negative": {"sentiment": 'negative'},
                     }

sentiments = types_of_sentiments.keys()

# Top text area
with st.container():
    # st.title("Sentiment Analisys")
    st.title("Reviews for the book \"Outliers: The Story of Success\"")

(column_1, column_2, column_3), test_data = st.columns(3), False
with column_1:
    visualization_chosen = st.selectbox("Data Visualization", visualizations, 0)
with column_2:
    sentiment_chosen = st.selectbox("Choose the sentiment", types_of_sentiments, 0)
with column_3:
    years = list(range(2015,2021))
    year = st.selectbox("Year", years, len(years)-1)
test = '_test' if test_data else ''

# print(f"Year: {year}")
# print(f"Test data: {test_data}")

# def replaceStarBy0or1(data):
#     # data['stars_processed'] = data['stars'].replace([[1,2],[3,4,5]],[0,1])

#     data['stars_processed'].map({1: 0, 2: 0, 3: 0, 4: 1, 5: 1})

#     return data

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

if visualization_chosen == 'Positive versus Negative':
    ddf = load_dataset_after_preprocessing().copy()
elif visualization_chosen == 'Wordcloud before preprocessing':
    ddf = load_dataset_before_preprocessing().copy()
    # print(len(ddf))
elif visualization_chosen == 'Worcloud after preprocessing':
    ddf = load_dataset_after_preprocessing().copy()
    # ddf = ddf.dropna(subset=['processing5'])
    # print(len(ddf))
elif visualization_chosen == 'Top 10 words before preprocessing':
    ddf = load_dataset_before_preprocessing().copy()
    # print(len(ddf))
elif visualization_chosen == 'Top 10 words after preprocessing':
    ddf = load_dataset_after_preprocessing().copy()
    # print(len(ddf))
elif visualization_chosen == 'Line chart':
    ddf = load_dataset_with_date().copy()
else:
    ddf = load_dataset_after_preprocessing().copy()


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
    ax.set_title("Sentiment through the time")
    ax.set_xlabel("Years")
    ax.set_ylabel("Number of Reviews")

    # Charmander
    sns.lineplot(ax=ax, x = res.index, y = res['positives'], color ='green', label='Positive')

    plt.show()
    st.pyplot(figure, use_container_width=True)
    return figure

def plot_animation(df):
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    new_reviews = [100, 80, 45, 32, 56, 23]
    old_reviews = new_reviews

    df.index = pd.to_datetime(df['date'], format='%Y-%m-%d')

    chart = st.line_chart(old_reviews)
    
    for i in range(1, 10):
        status_text.text("%i%% Complete" % i)

        new_reviews = [x + 3 for x in new_reviews]
        chart.add_rows(new_reviews)
        progress_bar.progress(i)
        old_reviews = new_reviews
        
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
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

def our_plot(params_visualization, params_sentiments, ddf_par, st):
    """ return plotly plots """
    
    if params_visualization["type"] == "line_chart":
        # plot_animation(ddf)
        plot_bar_graph_reviews_per_year(ddf)
    
    elif params_visualization["type"] == "pie_plot":
        print(len(ddf))
        pie_plot_sentiment(ddf)
     
    elif params_visualization["type"] == "wordCloud_before":
        if params_sentiments["sentiment"] == "positive":
            generate_wordcloud_sentiment(ddf, 'x', 1)
        elif params_sentiments["sentiment"] == "negative":
            generate_wordcloud_sentiment(ddf, 'x', 0)
    
    elif params_visualization["type"] == "wordCloud_after":
        if params_sentiments["sentiment"] == "positive":
            generate_wordcloud_sentiment(ddf, 'processing5', 1)
        elif params_sentiments["sentiment"] == "negative":
            generate_wordcloud_sentiment(ddf, 'processing5', 0)
        
    elif params_visualization["type"] == "barplot_before":
        if params_sentiments["sentiment"] == "positive":
            pltplot_high_frequence_words(ddf, 'x', 1, 10)
        elif params_sentiments["sentiment"] == "negative":
            pltplot_high_frequence_words(ddf, 'x', 0, 10)
    
    elif params_visualization["type"] == "barplot_after":
        if params_sentiments["sentiment"] == "positive":
            pltplot_high_frequence_words(ddf, 'processing5', 1, 10)
        elif params_sentiments["sentiment"] == "negative":
            pltplot_high_frequence_words(ddf, 'processing5', 0, 10)
    
    else:
        generate_wordcloud_sentiment(ddf, 'x', 1)
        
with st.container():
    print(visualization_chosen, sentiment_chosen)
    plot = our_plot(type_of_visualization[visualization_chosen], types_of_sentiments[sentiment_chosen], ddf, st)

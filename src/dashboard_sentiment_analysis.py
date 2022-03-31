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


# can only set this once, first thing to set
st.set_page_config()

type_of_visualization = {
    "Wordcloud without preprocessing": {"type": 'wordCloud'},
    "Worcloud with preprocessing": {"type": 'wordCloud'},
    "Top 10 words": {"type": "barplot"},
}

visualizations = type_of_visualization.keys()

types_of_sentiments = {"Positive": {"sentiment": 'positive'}, 
                    "Neutral": {"sentiment": 'neutral'},
                    "Negative": {"sentiment": 'negative'},
                     }

sentiments = types_of_sentiments.keys()

# Top text area
with st.container():
    # st.title("Sentiment Analisys")
    st.title("Reviews for the book: Outliers: The Story of Success")

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

# Get data before preprocessing
@st.cache()
def load_wordcloud_without_preprocessing():
    path = f'../dataset/graphs/df_concat_initial.csv'
    return pd.read_csv(path)#, columns=cols_used)

# Get data after preprocessing 1
@st.cache()
def load_wordcloud_with_preprocessing():
    path = f'../dataset/graphs/df_concat_initial.csv'
    return pd.read_csv(path)

# Get sta after preprocessing 2
@st.cache()
def load_top_10_words():
    path = f'../dataset/graphs/df_concat_initial.csv'
    return pd.read_csv(path)

if sentiment_chosen == 'Positive':
    ddf = load_wordcloud_without_preprocessing()
elif sentiment_chosen == 'Neutral':
    ddf = load_wordcloud_with_preprocessing()
elif sentiment_chosen == 'Negative':
    ddf = load_top_10_words()

else:
    ddf = load_wordcloud_without_preprocessing()


def generate_wordcloud_sentiment(text, target, sentiment):
    
    sentiment_text = text.query("y == " f'{sentiment}')

    all_words = ' '.join([text for text in sentiment_text[target]])

    wordCloud = WordCloud(width=400, height=250,
                            max_font_size=110).generate(all_words)

    print('---------------- all_words_size ---------------', len(all_words))
    figure = plt.figure(figsize=(10,7))
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.pyplot(figure, use_container_width=True)
    return figure

def pltplot_high_frequence_words(dataset, review_col, number_of_words):
    # nltk.download("all")
    all_words = ' '.join([dataset for dataset in dataset[review_col]])

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
    if params_visualization["type"] == "wordCloud":
        if params_sentiments["sentiment"] == "positive":
            generate_wordcloud_sentiment(ddf, 'x', 1)
        elif params_sentiments["sentiment"] == "neutral":
            generate_wordcloud_sentiment(ddf, 'x', 0)
        elif params_sentiments["sentiment"] == "negative":
            generate_wordcloud_sentiment(ddf, 'x', 0)
    else:
        pltplot_high_frequence_words(ddf, 'x', 15)
        
with st.container():
    plot = our_plot(type_of_visualization[visualization_chosen], types_of_sentiments[sentiment_chosen], ddf, st)

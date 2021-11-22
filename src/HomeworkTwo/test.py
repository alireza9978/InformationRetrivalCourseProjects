# nltk
import nltk
import numpy as np
import pandas as pd
import swifter
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

_ = swifter.config


def cleanData(movie):
    # upper case to lower case
    movie['cleanPlot'] = movie['plot'].map(lambda x: x.lower())
    # remove number
    movie['cleanPlot'] = movie['cleanPlot'].map(lambda x: re.sub(r'\d+', '', x))
    # remove punctuation
    movie['cleanPlot'] = movie['cleanPlot'].map(lambda x: re.sub(r'[^a-zA-Z]', ' ', x))
    # remove whitespace
    movie['cleanPlot'] = movie['cleanPlot'].map(lambda x: x.strip())
    # remove url
    url_cleaner = 'http\S+'
    movie['cleanPlot'] = movie['cleanPlot'].map(lambda x: re.sub(url_cleaner, ' ', x))
    # removing short words
    movie['cleanPlot'] = movie['cleanPlot'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))
    return movie


def tokenization(data):
    # Tokenization
    tokenized_overview = data['cleanPlot'].apply(lambda x: x.split())
    return tokenized_overview


# Removing stop words
def removeStopWord(tokenized_overview):
    stop_words = set(stopwords.words('english'))
    tokenized_overview = tokenized_overview.apply(lambda text: [word for word in text if word not in stop_words])
    return tokenized_overview


# Lemmatizing the words using WordNet
def Lemmatizing(tokenized_documents):
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N": wordnet.NOUN, "V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}

    def lemmatize_words(text):
        pos_tagged_text = nltk.pos_tag(text)
        # pos_tagged_text = text.apply(lambda x: nltk.pos_tag(x))
        return [lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text]

    tokenized_documents = tokenized_documents.apply(lambda text: lemmatize_words(text))
    return tokenized_documents


if __name__ == '__main__':
    stemmer = PorterStemmer()

    query_df = pd.read_csv("../../data/HW2/Queries.csv")
    query_df = cleanData(query_df)
    tokenized_plot = tokenization(query_df)
    tokenized_plot = removeStopWord(tokenized_plot)
    tokenized_plot = tokenized_plot.apply(lambda x: [stemmer.stem(i) for i in x])
    tokenized_plot = Lemmatizing(tokenized_plot)

    all_words_set = sorted(set(np.concatenate(tokenized_plot.to_list()).tolist()))


    def vectorise(temp_list):
        result = np.unique(temp_list, return_counts=True)
        plot_words = dict(zip(result[0], result[1]))
        return pd.Series(plot_words, index=all_words_set)


    temp_df = tokenized_plot.swifter.apply(vectorise)
    temp_df = temp_df.swifter.apply(lambda x: x / x.sum())
    print(temp_df)

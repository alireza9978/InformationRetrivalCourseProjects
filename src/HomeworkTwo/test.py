from pathlib import Path

import nltk
import pandas as pd
import swifter
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    movie['cleanPlot'] = movie['cleanPlot'].swifter.apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))
    return movie


def tokenization(data):
    # Tokenization
    tokenized_overview = data['cleanPlot'].swifter.apply(lambda x: x.split())
    return tokenized_overview


# Removing stop words
def removeStopWord(tokenized_overview):
    stop_words = set(stopwords.words('english'))
    tokenized_overview = tokenized_overview.swifter.apply(
        lambda text: [word for word in text if word not in stop_words])
    return tokenized_overview


# Lemmatizing the words using WordNet
def Lemmatizing(tokenized_documents):
    lemmatizer = WordNetLemmatizer()
    wordnet_map = {"N": wordnet.NOUN, "V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}

    def lemmatize_words(text):
        pos_tagged_text = nltk.pos_tag(text)
        # pos_tagged_text = text.apply(lambda x: nltk.pos_tag(x))
        return [lemmatizer.lemmatize(word, wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_tagged_text]

    tokenized_documents = tokenized_documents.swifter.apply(lambda text: lemmatize_words(text))
    return tokenized_documents


def read_file(path):
    dataset_path = Path(path)
    with open(dataset_path) as f:
        lines = f.readlines()

    dataset = pd.DataFrame(lines, columns=["raw_data"])
    dataset["raw_data"] = dataset["raw_data"].swifter.apply(lambda row: row.split("\t"))
    dataset = pd.DataFrame(dataset['raw_data'].to_list(), columns=['id', 'plot'])
    return dataset


def preprocess_df(temp_df):
    stemmer = PorterStemmer()
    temp_df = cleanData(temp_df)
    tokenized_plot = tokenization(temp_df)
    tokenized_plot = removeStopWord(tokenized_plot)
    tokenized_plot = tokenized_plot.swifter.apply(lambda x: [stemmer.stem(i) for i in x])
    tokenized_plot = Lemmatizing(tokenized_plot)
    string_plot = tokenized_plot.swifter.apply(lambda x: " ".join(x))
    return string_plot


if __name__ == '__main__':
    main_df = read_file("../../data/HW1/plot_summaries.txt")
    query_df = pd.read_csv("../../data/HW2/Queries.csv")

    main_df_cleaned = preprocess_df(main_df)
    query_df_cleaned = preprocess_df(query_df)

    model = TfidfVectorizer()
    tf_idf_plots = model.fit_transform(main_df_cleaned.to_list())
    tf_idf_queries = model.transform(query_df_cleaned.to_list())
    distances = cosine_similarity(tf_idf_queries, tf_idf_plots)
    for i, row in enumerate(distances):
        main_df.loc[row.argsort()[:5]].to_csv("../../result/similar_plots/query_{}_similar_plots.csv".format(i + 1),
                                              index=False)

    # calculate distance with old method
    # all_words_set = sorted(set(np.concatenate(all_df_tokenized.to_list()).tolist()))
    # def vectorise(temp_list):
    #     result = np.unique(temp_list, return_counts=True)
    #     plot_words = dict(zip(result[0], result[1]))
    #     return pd.Series(plot_words, index=all_words_set)
    # tf_df = all_df_tokenized.swifter.apply(vectorise)
    # tf_idf_df = tf_df.swifter.apply(lambda x: x / x.sum())
    # # queries tf.idf
    # queries_tf_idf = tf_idf_df.iloc[0:10]
    # # plots tf.idf
    # plots_tf_idf = tf_idf_df.iloc[11:]
    # print(plots_tf_idf)
    # distances = cosine_similarity(queries_tf_idf, plots_tf_idf)
    # print(distances)

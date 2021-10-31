import re

from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords

porter_stemmer = PorterStemmer()
word_net = WordNetLemmatizer()


# Remove all punctuations from the text [!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]:
def remove_punctuation(temp_text: str) -> str:
    return re.sub(r'[^a-zA-Z]', ' ', temp_text)


# Remove all url from the text
def clean_url(temp_text: str) -> str:
    return re.sub(r'http\S+', '', temp_text)


def make_lower(temp_text: str) -> str:
    return temp_text.lower()


# tokenize text
def tokenize(temp_text: str) -> list:
    return word_tokenize(temp_text)


# Remove short tokens
def remove_short_tokens(temp_tokens: list) -> list:
    return [word for word in temp_tokens if len(word) > 2]


# Remove stopwords
def remove_stopwords(temp_tokens: list) -> list:
    return [word for word in temp_tokens if word not in stopwords.words('english')]


# Apply stemming to get root words
def stemming(temp_tokens: list) -> list:
    return [porter_stemmer.stem(word) for word in temp_tokens]


# Apply lemmatization on tokens
def lemmatize(temp_tokens: list) -> list:
    return [word_net.lemmatize(word) for word in temp_tokens]


if __name__ == '__main__':
    sample_text = "As we can see there is an url and we don’t want it to be " \
                  "a part of our corpus. https://google.com Let’s remove it by using below line of code."
    sample_text = remove_punctuation(sample_text)
    sample_text = clean_url(sample_text)
    sample_text = make_lower(sample_text)
    sample_text_tokens = tokenize(sample_text)
    sample_text_tokens = remove_short_tokens(sample_text_tokens)
    sample_text_tokens = remove_stopwords(sample_text_tokens)
    sample_text_tokens = stemming(sample_text_tokens)
    sample_text_tokens = lemmatize(sample_text_tokens)
    print(sample_text_tokens)

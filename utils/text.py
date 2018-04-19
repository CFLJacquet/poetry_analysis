import treetaggerwrapper as ttw
import pandas
from nltk.corpus import stopwords as sw
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
import json
import nltk
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline


def lower(words):
    return words.lower()


def tokenize(words):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(words)
    return tokens


def filter_words(tokens):
    my_stopwords = ['tout', 'si']
    customized_stopwords = stopwords.words('french') + my_stopwords
    filtered_words = [w for w in tokens if not w in customized_stopwords]
    return filtered_words


def remove_punkts(sentence):
    sentence = lower(sentence)
    tokens = tokenize(sentence)
    filtered_words = filter_words(tokens)
    return " ".join(filtered_words)


def get_lemmatized_sentence(sentence):
    sentence = lower(sentence)
    without_punkts = remove_punkts(sentence)
    tokens = tokenize(without_punkts)
    filtered = filter_words(tokens)
    return ' '.join(filtered)


def get_tfidf(list_of_texts):
    tfidf_transformer = TfidfVectorizer(list_of_texts, encoding='utf-8')
    tfidf_matrix = tfidf_transformer.fit_transform(list_of_texts)
    return tfidf_matrix


def get_count(list_of_texts):
    count_vec = CountVectorizer(list_of_texts, encoding='utf-8')
    return count_vec.fit_transform(list_of_texts)


def load_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data


def get_json_dataframe(json):
    return pandas.DataFrame(json)


if __name__=="__main__":
    phrase = "J'ai consacré ma vie à la musique"
    print(lower(phrase))
    token = tokenize(phrase)
    print(token)
    print(filter_words(token))
    print(get_lemmatized_sentence(phrase))
    print(get_tfidf(["salut c'est cool", "oui", "c'est bien vvrai"]))

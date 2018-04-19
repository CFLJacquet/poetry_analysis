import treetaggerwrapper as ttw
from nltk.corpus import stopwords as sw
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from utils.text import get_lemmatized_sentence, load_json, get_tfidf
import json
import nltk


def preprocess(raw_docs_json, stopwords_list=None):
    """ Input : path to poems in json format\n
                path to stopwords list as doc file, one word per row
        Return : list of lemmatized poems
    """

    tagger = ttw.TreeTagger(TAGLANG='fr')
    stopwords = set(sw.words('french')) if stopwords_list==None else open(stopwords_list, 'r', encoding='utf-8').read().split("\n")

    with open(raw_docs_json, "r") as f:
        raw_documents = json.load(f)

    processed_docs = [lemmatizer(tagger, elt["text"], stopwords) for elt in raw_documents]

    return processed_docs


def lemmatizer(tagger, document, stopwords):
    """ Given a text files, returns the text with lemmatized words """
    tags = tagger.tag_text(document)
    lemmatized_doc = []

    for elt in tags:
        clean = elt.split('\t')
        try:
            if clean[2] not in stopwords:
                lemmatized_doc.append(str(clean[2]))
        except:
            pass
    return " ".join(lemmatized_doc)


def preprocess_nltk(raw_docs_json):
    """ Input : path to poems in json format\n
                path to stopwords list as doc file, one word per row
        Return : list of lemmatized poems
    """
    raw_documents = load_json(raw_docs_json)

    filtered_docs = []
    for document in raw_documents:
        new_doc = get_lemmatized_sentence('\n'.join(document['text']))
        filtered_docs.append(new_doc)
    return filtered_docs


def json_to_tfidf(json_path):
    data = load_json(json_path)
    tfidf = get_tfidf(data)
    return tfidf


if __name__ == "__main__":
    '''a = preprocess("poems_extracted.json")
    print(a[0])
    with open("./data/poems_text.json", "w") as f:
        json.dump(a, f)
    '''

    processed = preprocess_nltk('./data/poems_extracted.json')
    print(processed[0])
    with open('./data/poems_text_anais.json', 'w') as f:
        json.dump(processed, f)

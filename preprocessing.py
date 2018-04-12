import treetaggerwrapper as ttw
from nltk.corpus import stopwords as sw
import json
from pprint import pprint

def preprocess(raw_docs_json, stopwords_list=None):
    """ Input : path to poems in json format\n
                path to stopwords list as doc file, one word per row
        Return : list of lemmatized poems
    """

    tagger = ttw.TreeTagger(TAGLANG='fr')
    stopwords = set(sw.words('french')) if stopwords_list==None else open(stopwords_list, 'r', encoding='utf-8').read().split("\n")

    processed_docs = []
    with open(raw_docs_json, "r") as f :
        raw_documents = json.load(f)

    processed_docs = [lemmatizer(tagger, "\n".join(elt["text"]), stopwords) for elt in raw_documents]

    return processed_docs




def lemmatizer(tagger, document, stopwords):
    """ Given a text files, returns the text with lemmatized words """
    
    tags = tagger.tag_text(document)
    lemmatized_doc = []

    for elt in tags:
        clean = elt.split('\t')
        try :
            if clean[2] not in stopwords:
                lemmatized_doc.append(str(clean[2]))
        except:
            pass
    return " ".join(lemmatized_doc)


if __name__ == "__main__":
    a = preprocess("poems_extracted.json")
    print(a[0])
    with open("poems_text.json", "w") as f:
        json.dump(a, f)






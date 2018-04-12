import string

import treetaggerwrapper as ttw

from nltk.corpus import stopwords as sw
from nltk.corpus import wordnet as wn
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag

from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.feature_extraction.text import CountVectorizer





class CountVectPreprocessor(CountVectorizer):
        def fit_transform(self, raw_documents, y=None):
        """Learn the vocabulary dictionary and return term-document matrix.

        This is equivalent to fit followed by transform, but more efficiently
        implemented.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.

        Returns
        -------
        X : array, [n_samples, n_features]
            Document-term matrix.
        """
        # We intentionally don't call the transform method to make
        # fit_transform overridable without unwanted side effects in
        # TfidfVectorizer.
        if isinstance(raw_documents, six.string_types):
            raise ValueError(
                "Iterable over raw text documents expected, "
                "string object received.")

        self._validate_vocabulary()
        max_df = self.max_df
        min_df = self.min_df
        max_features = self.max_features

        # ---------------------------------------------------------------
        # Modifications to preprocess docs (lemmatization)
        # ---------------------------------------------------------------
        processed_docs = self.preprocess(raw_documents)

        vocabulary, X = self._count_vocab(processed_docs,
                                          self.fixed_vocabulary_)
        # ---------------------------------------------------------------

        if self.binary:
            X.data.fill(1)

        if not self.fixed_vocabulary_:
            X = self._sort_features(X, vocabulary)

            n_doc = X.shape[0]
            max_doc_count = (max_df
                             if isinstance(max_df, numbers.Integral)
                             else max_df * n_doc)
            min_doc_count = (min_df
                             if isinstance(min_df, numbers.Integral)
                             else min_df * n_doc)
            if max_doc_count < min_doc_count:
                raise ValueError(
                    "max_df corresponds to < documents than min_df")
            X, self.stop_words_ = self._limit_features(X, vocabulary,
                                                       max_doc_count,
                                                       min_doc_count,
                                                       max_features)

            self.vocabulary_ = vocabulary

        return X

    def transform(self, raw_documents):
        """Transform documents to document-term matrix.

        Extract token counts out of raw text documents using the vocabulary
        fitted with fit or the one provided to the constructor.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.

        Returns
        -------
        X : sparse matrix, [n_samples, n_features]
            Document-term matrix.
        """
        if isinstance(raw_documents, six.string_types):
            raise ValueError(
                "Iterable over raw text documents expected, "
                "string object received.")

        if not hasattr(self, 'vocabulary_'):
            self._validate_vocabulary()

        self._check_vocabulary()

        # use the same matrix-building strategy as fit_transform

        # ---------------------------------------------------------------
        # Modifications to preprocess docs (lemmatization)
        # ---------------------------------------------------------------
        processed_docs = self.preprocess(raw_documents)
        _, X = self._count_vocab(processed_docs, fixed_vocab=True)
        # ---------------------------------------------------------------
        
        if self.binary:
            X.data.fill(1)
        return X

    def preprocess(self, raw_documents):
        processed_docs = []

        for elt in raw_documents:
            

        return processed_docs



class NLTKPreprocessor(BaseEstimator, TransformerMixin):

    tagger = ttw.TreeTagger(TAGLANG='fr')

    def __init__(self, stopwords=None, punct=None,lower=True, strip=True):
        self.lower      = lower
        self.strip      = strip
        self.stopwords  = stopwords or set(sw.words('french'))
        self.punct      = punct or set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, X):
        return [
            " ".join(list(self.tokenize(doc))) for doc in X
        ]

    def fit_transform(self, X, y=None):
        return self.transform(X)

    def tokenize(self, document):
        
        tags = NLTKPreprocessor.tagger.tag_text(document)

        for elt in tags:
            clean = elt.split('\t')
            try :
                if clean[2] not in self.stopwords:
                    yield clean[2]
            except:
                pass


    #     # Break the document into sentences
    #     for sent in sent_tokenize(document):
    #         # Break the sentence into part of speech tagged tokens
    #         for token, tag in pos_tag(wordpunct_tokenize(sent)):
    #             # Apply preprocessing to the token
    #             token = token.lower() if self.lower else token
    #             token = token.strip() if self.strip else token
    #             token = token.strip('_') if self.strip else token
    #             token = token.strip('*') if self.strip else token

    #             # If stopword, ignore token and continue
    #             if token in self.stopwords:
    #                 continue

    #             # If punctuation, ignore token and continue
    #             if all(char in self.punct for char in token):
    #                 continue

    #             # Lemmatize the token and yield
    #             lemma = self.lemmatize(token, tag)
    #             yield lemma

    # def lemmatize(self, token, tag):
    #     tag = {
    #         'N': wn.NOUN,
    #         'V': wn.VERB,
    #         'R': wn.ADV,
    #         'J': wn.ADJ
    #     }.get(tag[0], wn.NOUN)

    #     return self.lemmatizer.lemmatize(token, tag)

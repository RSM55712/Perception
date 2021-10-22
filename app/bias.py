import tensorflow as tf
from tensorflow import keras
import numpy as np
import re
import string
from collections import Counter
import pickle
import nltk

punctuation_regex = re.compile("[{}]".format(re.escape(string.punctuation)))


def strip_punctuation(corpus):
    return punctuation_regex.sub("", corpus)


def parse_article(article):
    stop_words = [
        "ourselves",
        "hers",
        "between",
        "yourself",
        "but",
        "again",
        "there",
        "about",
        "once",
        "during",
        "out",
        "very",
        "having",
        "with",
        "they",
        "own",
        "an",
        "be",
        "some",
        "for",
        "not",
        "its",
        "yours",
        "such",
        "into",
        "of",
        "most",
        "itself",
        "other",
        "off",
        "is",
        "s",
        "am",
        "or",
        "who",
        "as",
        "from",
        "him",
        "each",
        "the",
        "themselves",
        "until",
        "below",
        "are",
        "we",
        "these",
        "your",
        "his",
        "through",
        "done",
        "nor",
        "me",
        "were",
        "her",
        "more",
        "himself",
        "this",
        "down",
        "should",
        "our",
        "their",
        "while",
        "above",
        "both",
        "up",
        "to",
        "ours",
        "had",
        "she",
        "all",
        "no",
        "when",
        "at",
        "any",
        "before",
        "them",
        "same",
        "and",
        "been",
        "have",
        "in",
        "will",
        "on",
        "does",
        "yourselves",
        "then",
        "that",
        "because",
        "what",
        "over",
        "why",
        "so",
        "can",
        "did",
        "not",
        "now",
        "under",
        "he",
        "you",
        "herself",
        "has",
        "just",
        "where",
        "too",
        "only",
        "myself",
        "which",
        "those",
        "i",
        "after",
        "few",
        "whom",
        "t",
        "being",
        "if",
        "theirs",
        "my",
        "against",
        "a",
        "by",
        "doing",
        "it",
        "how",
        "further",
        "was",
        "here",
        "than",
    ]

    stripped = strip_punctuation(article)
    cleaned = "".join(i for i in stripped if ord(i) < 128)

    count = Counter(strip_punctuation(cleaned).lower().split())
    count_filtered = dict()

    for i, k in enumerate(count.keys()):
        if i > 40:
            break

        if k not in stop_words:
            count_filtered.update({k: count[k]})

    return count_filtered


def load_unique():
    with open("data/unique.pkl", "rb") as un:
        unique = pickle.load(un)

    return unique


def format_data(data, unique):
    formatted = np.zeros((len(unique)))
    for t in data.keys():
        try:
            formatted[unique.index(t)] = data[t]
        except:
            pass

    return np.asarray([formatted])


def load_model():
    with open("data/model.json", "r") as json_file:
        model_json = json_file.read()

    model = keras.models.model_from_json(model_json)

    model.load_weights("data/model.h5")

    model.compile(
        optimizer=keras.optimizers.Adam(
            lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False
        ),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model

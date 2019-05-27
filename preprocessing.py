# if spacy.load(lang) doesn't work run spacy_ext.sh

import pickle
import spacy
from pymystem3 import Mystem
import re


def clean_twitter_data(texts):
    return [re.sub(r"(?:\@|https?\://)\S+", "", text) for text in texts]


def get_data(what):
    assert what in ['ted', 'twitter', 'dicts']
    if what is 'ted':
        with open("./data/ted/ted_parallel_en.pkl", "rb") as f:
            data_en = pickle.load(f)
            data_en = [text.replace("\n", " ") for text in data_en]

        with open("./data/ted/ted_parallel_fr.pkl", "rb") as f:
            data_fr = pickle.load(f)
            data_fr = [text.replace("\n", " ") for text in data_fr]

        with open("./data/ted/ted_parallel_ru.pkl", "rb") as f:
            data_ru = pickle.load(f)
            data_ru = [text.replace("\n", " ") for text in data_ru]

        return data_en, data_fr, data_ru

    if what is 'twitter':
        with open("./data/twitter/greenpeaceusa.pkl", "rb") as f:
            data_en = pickle.load(f)
            data_en = [pair[1].replace("\n", " ") for pair in data_en]
            data_en = clean_twitter_data(data_en)

        with open("./data/twitter/greenpeacefr.pkl", "rb") as f:
            data_fr = pickle.load(f)
            data_fr = [pair[1].replace("\n", " ") for pair in data_fr]
            data_fr = clean_twitter_data(data_fr)

        with open("./data/twitter/greenpeaceru.pkl", "rb") as f:
            data_ru = pickle.load(f)
            data_ru = [pair[1].replace("\n", " ") for pair in data_ru]
            data_ru = clean_twitter_data(data_ru)

        return data_en, data_fr, data_ru


def lemmatize(texts, lang):
    assert lang in ['fr', 'en', 'ru']
    if lang is 'ru':
        m = Mystem()
        texts_lem = ["".join(m.lemmatize(text)) for text in texts]
    else:
        nlp = spacy.load(lang)
        texts_lem = [" ".join([w.lemma_ for w in nlp(text)]) for text in texts]
    texts_lem = [text.replace("\n", " ") for text in texts_lem]
    return texts_lem


def preprocess_texts():
    ted_en, ted_fr, ted_ru = get_data(what="ted")
    twitter_en, twitter_fr, twitter_ru = get_data(what="twitter")

    print("Loaded files")

    ted_en = lemmatize(ted_en, lang="en")
    ted_fr = lemmatize(ted_fr, lang="fr")
    ted_ru = lemmatize(ted_ru, lang="ru")

    print("Lemmatized ted data")

    twitter_en = lemmatize(twitter_en, lang="en")
    twitter_fr = lemmatize(twitter_fr, lang="fr")
    twitter_ru = lemmatize(twitter_ru, lang="ru")

    print("Lemmatized twitter data")

    with open("./data/preprocessed/ted/ted_en.pkl", 'wb') as f:
        pickle.dump(ted_en, f)

    with open("./data/preprocessed/ted/ted_fr.pkl", 'wb') as f:
        pickle.dump(ted_fr, f)

    with open("./data/preprocessed/ted/ted_ru.pkl", 'wb') as f:
        pickle.dump(ted_ru, f)

    with open("./data/preprocessed/twitter/twitter_en.pkl", 'wb') as f:
        pickle.dump(twitter_en, f)

    with open("./data/preprocessed/twitter/twitter_fr.pkl", 'wb') as f:
        pickle.dump(twitter_fr, f)

    with open("./data/preprocessed/twitter/twitter_ru.pkl", 'wb') as f:
        pickle.dump(twitter_ru, f)

    print("Saved all the preprocessed files to the ./data/preprocessed dir")


preprocess_texts()


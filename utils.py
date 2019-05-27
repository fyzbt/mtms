import pickle
from sklearn.feature_extraction.text import CountVectorizer


def read_data(need_dict=False):
    with open("./data/preprocessed/ted/ted_en.pkl", "rb") as f:
        ted_en = pickle.load(f)

    with open("./data/preprocessed/ted/ted_fr.pkl", "rb") as f:
        ted_fr = pickle.load(f)

    with open("./data/preprocessed/ted/ted_ru.pkl", "rb") as f:
        ted_ru = pickle.load(f)

    with open("./data/preprocessed/twitter/twitter_en.pkl", "rb") as f:
        twitter_en = pickle.load(f)

    with open("./data/preprocessed/twitter/twitter_fr.pkl", "rb") as f:
        twitter_fr = pickle.load(f)

    with open("./data/preprocessed/twitter/twitter_ru.pkl", "rb") as f:
        twitter_ru = pickle.load(f)

    if need_dict:
        with open("./data/dicts/EN_FR.pkl", "rb") as f:
            dict_en_fr = pickle.load(f)

        with open("./data/dicts/EN_RU.pkl", "rb") as f:
            dict_en_ru = pickle.load(f)

        return ted_en, ted_fr, ted_ru, twitter_en, twitter_fr, twitter_ru, dict_en_fr, dict_en_ru

    else:
        return ted_en, ted_fr, ted_ru, twitter_en, twitter_fr, twitter_ru


def texts_to_tdm(texts):
    """
    converts list of texts to term-document-matrix
    :param texts: list of texts
    :return: sparse matrix and feature names
    """
    cv = CountVectorizer(lowercase=True, ngram_range=(1, 1))
    return cv.fit_transform(texts), cv.get_feature_names()


def clean_dict(dictionary, vocab_src, vocab_trans, lang, write=False):
    ind_map_src = {vocab_src[i]: i for i in range(len(vocab_src))}
    ind_map_trans = {vocab_trans[i]: i for i in range(len(vocab_trans))}

    dictionary = [[ind_map_src[pair[0]], ind_map_trans[pair[1]]] for pair in dictionary if
                  pair[0] in vocab_src and
                  pair[1] in vocab_trans]

    if write:
        import pickle
        with open(f"./data/dicts/clean_dict_en_{lang}.pkl", "wb") as f:
            pickle.dump(dictionary, f)

    else:
        return dictionary, ind_map_src, ind_map_trans


def prepare_data_for_pltm():
    ted_en, ted_fr, ted_ru, twitter_en, twitter_fr, twitter_ru = read_data(need_dict=False)

    # hardcoding texts with non-utf chars (otherwise pltm drops erroe while processing french)
    ted_en.pop(573)
    ted_en.pop(906)
    ted_fr.pop(573)
    ted_fr.pop(906)
    ted_ru.pop(573)
    ted_ru.pop(906)

    twitter_en = [text.replace("\n", " ")for text in twitter_en]
    twitter_fr = [text.replace("\n", " ")for text in twitter_fr]
    twitter_ru = [text.replace("\n", " ") for text in twitter_ru]

    with open('./data/preprocessed/ted/ted_en.txt', 'w') as f:
        for item in ted_en:
            f.write("%s\n" % item)

    with open('./data/preprocessed/ted/ted_fr.txt', 'w') as f:
        for item in ted_fr:
            f.write("%s\n" % item)

    with open('./data/preprocessed/ted/ted_ru.txt', 'w') as f:
        for item in ted_ru:
            f.write("%s\n" % item)

    print("Added txt files of ted files to ./data/preprocessed/ted")

    with open('./data/preprocessed/twitter/twitter_en.txt', 'w') as f:
        for item in twitter_en[:3098]:
            f.write("%s\n" % item)

    with open('./data/preprocessed/twitter/twitter_fr.txt', 'w') as f:
        for item in twitter_fr[:3099]:
            f.write("%s\n" % item)

    with open('./data/preprocessed/twitter/twitter_ru.txt', 'w') as f:
        for item in twitter_ru[:3100]:
            f.write("%s\n" % item)

    print("Added txt files of twitter files to ./data/preprocessed/twitter")


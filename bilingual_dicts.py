import requests
import pickle

DICT_URLS = {
    "EN_FR": "https://github.com/open-dsl-dict/wiktionary-dict/blob/master/src/en-fr-enwiktionary.txt?raw=true",
    "EN_RU": "https://github.com/open-dsl-dict/wiktionary-dict/blob/master/src/en-ru-enwiktionary.txt?raw=true"
}


def parse_dict(url):
    data = requests.get(url).text
    data = data.split("\n")

    transl = []
    for line in data:
        if "#" not in line and len(line) > 0 and " :: " in line:
            key, val = line.split(" :: ")
            key = key.split(" {")[0].lower()
            val = val.split(" {")[0].lower()
            if " " not in key and " " not in val:
                transl.append([key, val])
    return transl


def write_dict(data, lang):
    with open(f"./data/dicts/{lang}.pkl", "wb") as f:
        pickle.dump(data, f)


def get_dict(urls):
    for key in list(urls):
        words = parse_dict(urls[key])
        write_dict(words, key)


get_dict(DICT_URLS)


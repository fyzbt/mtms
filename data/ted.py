from bs4 import BeautifulSoup
import lxml
import pickle
import pandas as pd

FILE_PATHS = {
    "ru": "/Users/macbook/Downloads/FILTERED_xml/ted_ru.xml",
    "en": "/Users/macbook/Downloads/FILTERED_xml/ted_en.xml",
    "fr": "/Users/macbook/Downloads/FILTERED_xml/ted_fr.xml"
}


def parse_talk_xml(data):
    tree = BeautifulSoup(data, features="lxml")
    talk_data = {}
    vids = tree.find_all("file")
    for vid in vids:
        if vid.talkid is None:
            continue
        url = vid.url.text
        talk_id = vid.talkid.text
        if vid.speaker:
            speaker = vid.speaker.text
        if vid.keywords:
            keywords = vid.keywords.text
        if vid.date:
            date = vid.date.text
        else:
            continue
        if vid.description:
            description = vid.description.text
        else:
            continue
        if vid.transcription:
            transcription = [i.text for i in vid.find_all("seekvideo")]
            talk_data[talk_id] = {
                "url": url, "keywords": keywords, "speaker": speaker,
                "date": date, "description": description, "transcription": transcription}
        else:
            continue
    return talk_data


def get_ted_data(file_paths=FILE_PATHS, include_meta=False):
    assert isinstance(file_paths, dict)
    for k in file_paths.keys():
        with open(file_paths[k]) as f:
            data = f.read()

        talks_meta = parse_talk_xml(data)
        ids = list(talks_meta.keys())
        texts = [[i, " ".join(talks_meta[i]['transcription'])] for i in ids]
        with open(f"./data/ted/ted_{k}.pkl", 'wb') as f:
            pickle.dump(texts, f)
        print(f"Texts are successfully saved to {str(f)}")

        if include_meta:
            with open(f"./data/ted/ted_meta_{k}.pkl", 'wb') as f:
                pickle.dump(talks_meta, f)
            print(f"Talks meta is successfully saved to {str(f)}")


def get_parallel_ted_data(**kwargs):
    get_ted_data(**kwargs)

    with open("./data/ted/ted_en.pkl", "rb") as f:
        ted_en = pickle.load(f)

    with open("./data/ted/ted_fr.pkl", "rb") as f:
        ted_fr = pickle.load(f)

    with open("./data/ted/ted_ru.pkl", "rb") as f:
        ted_ru = pickle.load(f)

    df_en = pd.DataFrame(ted_en)
    df_fr = pd.DataFrame(ted_fr)
    df_ru = pd.DataFrame(ted_ru)
    df_all = pd.merge(df_en, df_fr, on=0, how='inner')
    df_all = pd.merge(df_all, df_ru, on=0, how='inner')
    df_all.columns = ['talk_id', 'en', 'fr', 'ru']

    with open(f"./data/ted/ted_parallel_fr.pkl", 'wb') as f:
        pickle.dump(df_all.fr.tolist(), f)
    with open(f"./data/ted/ted_parallel_en.pkl", 'wb') as f:
        pickle.dump(df_all.en.tolist(), f)
    with open(f"./data/ted/ted_parallel_ru.pkl", 'wb') as f:
        pickle.dump(df_all.ru.tolist(), f)
    print("Loaded all the parallel data to the /data/ted folder")


get_parallel_ted_data()

from utils import read_data, texts_to_tdm, clean_dict
import anchor_topic.topics
import pickle
import numpy as np

ted_en, ted_fr, ted_ru, twitter_en, twitter_fr, twitter_ru, dict_en_fr, dict_en_ru = read_data(need_dict=True)

ted_en, voc_en = texts_to_tdm(ted_en)
ted_fr, voc_fr = texts_to_tdm(ted_fr)
ted_ru, voc_ru = texts_to_tdm(ted_ru)

twitter_en, voc_twi_en = texts_to_tdm(twitter_en)
twitter_fr, voc_twi_fr = texts_to_tdm(twitter_fr)
twitter_ru, voc_twi_ru = texts_to_tdm(twitter_ru)

# test version for en_ru ted data

dictionary, ind_map_en, ind_map_fr = clean_dict(dictionary=dict_en_fr, vocab_src=voc_twi_en,
                                                vocab_trans=voc_twi_fr, lang="fr")

M1 = twitter_en.transpose()
M2 = twitter_fr.transpose()

k = 30
threshold1 = 0.01
threshold2 = 0.01

A1, A2, Q1, Q2, anchors1, anchors2 = anchor_topic.topics.model_multi_topics(M1, M2, k,
                                                                            threshold1, threshold2,
                                                                            dictionary)

ind_maps_en_fr = [ind_map_en, ind_map_fr]

with open("./data/dicts/ind_maps_twitter_en_fr.pkl", 'wb') as f:
    pickle.dump(ind_maps_en_fr, f)

objs = [A1, A2, Q1, Q2, anchors1, anchors2]
obj_names = ["A1", "A2", "Q1", "Q2", "anchors1", "anchors2"]

for ind in range(len(objs)):
    if obj_names[ind] in ["A1", "A2", "Q1", "Q2"]:
        np.save(f"./results/mcta_twitter_30_en_fr_{obj_names[ind]}.npy", objs[ind])
    else:
        with open(f"./results/mcta_twitter_30_en_fr_{obj_names[ind]}.txt", 'w') as f:
            f.write(str(objs[ind]))


dictionary, ind_map_en, ind_map_ru = clean_dict(dictionary=dict_en_fr, vocab_src=voc_twi_en,
                                                vocab_trans=voc_twi_ru, lang="ru")

M1 = twitter_en.transpose()
M2 = twitter_ru.transpose()

k = 30
threshold1 = 0.0005
threshold2 = 0.0005

A1, A2, Q1, Q2, anchors1, anchors2 = anchor_topic.topics.model_multi_topics(M1, M2, k,
                                                                            threshold1, threshold2,
                                                                            dictionary)

ind_maps_en_ru = [ind_map_en, ind_map_ru]

with open("./data/dicts/ind_maps_twitter_en_ru.pkl", 'wb') as f:
    pickle.dump(ind_maps_en_ru, f)

objs = [A1, A2, Q1, Q2, anchors1, anchors2]
obj_names = ["A1", "A2", "Q1", "Q2", "anchors1", "anchors2"]

for ind in range(len(objs)):
    if obj_names[ind] in ["A1", "A2", "Q1", "Q2"]:
        np.save(f"./results/mcta_twitter_30_en_ru_{obj_names[ind]}.npy", objs[ind])
    else:
        with open(f"./results/mcta_twitter_30_en_ru_{obj_names[ind]}.txt", 'w') as f:
            f.write(str(objs[ind]))




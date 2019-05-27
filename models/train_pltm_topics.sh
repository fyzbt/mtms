#!/usr/bin/env bash

# going to the dir where mallet is
cd /Users/macbook/Downloads/mallet-2.0.8

./bin/mallet import-file --input /Users/macbook/multilingual_tm/data/preprocessed/ted/ted_ru.txt \
 --stoplist-file ./stoplists/ru.txt --output ru.sequences --keep-sequence \
  --token-regex '\p{L}+' --print-output

./bin/mallet import-file --input /Users/macbook/multilingual_tm/data/preprocessed/ted/ted_en.txt \
 --stoplist-file ./stoplists/en.txt --output en.sequences --keep-sequence \
  --token-regex '\p{L}+' --print-output


./bin/mallet import-file --input /Users/macbook/multilingual_tm/data/preprocessed/ted/ted_fr.txt \
 --stoplist-file ./stoplists/fr.txt --output fr.sequences --keep-sequence \
  --token-regex '\p{L}+' --print-output

#train model
./bin/mallet run cc.mallet.topics.PolylingualTopicModel \
  --language-inputs ru.sequences en.sequences fr.sequences \
  --num-topics 30 --alpha 1.0


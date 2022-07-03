from collections import defaultdict
import re
import sys

import fasttext

WORK_DIR = "/Users/dwinston/datasets/search_with_ml/fasttext/"

model = fasttext.load_model(WORK_DIR + "title_model.bin")

synonyms = []

with open(WORK_DIR + "top_words.txt", "r") as f:
    for line in f:
        word = line.strip()
        keeping = []
        for similarity, neighbor in model.get_nearest_neighbors(word):
            if similarity >= 0.75:
                keeping.append(neighbor)
        synonyms.append([word] + keeping)

with open(WORK_DIR + "synonyms.csv", "w") as fout:
    for entry in synonyms:
        fout.write(",".join(entry) + "\n")
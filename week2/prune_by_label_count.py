from collections import defaultdict
import re
import sys

WORK_DIR = "/Users/dwinston/datasets/search_with_ml/fasttext/"

THRESHOLD = int(sys.argv[1] if len(sys.argv) == 2 else 500)

line_pattern = re.compile(r"__label__([^ ]+)")

titles_by_label = defaultdict(list)

with open(WORK_DIR + "labeled_products.txt", "r") as f:
    for line in f:
        label = line_pattern.match(line).group(1)
        titles_by_label[label].append(line)

with open(WORK_DIR + "pruned_labeled_products.txt", "w") as f:
    for label, lines in titles_by_label.items():
        if len(lines) >= THRESHOLD:
            for line in lines:
                f.write(line)
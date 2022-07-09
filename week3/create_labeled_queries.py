import os
import argparse
import re
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.snowball.SnowballStemmer("english")

DATASETS_DIR = "/Users/dwinston/datasets/search_with_ml"

categories_file_name = rf'{DATASETS_DIR}/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = rf'{DATASETS_DIR}/train.csv'
output_file_name = rf'{DATASETS_DIR}/labeled_query_data.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

min_queries = int(args.min_queries)

print("min queries", min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

print("tabling category parents...")
# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
def normalize(query):
    rv = query.lower()
    # strip quotation marks
    rv = rv.replace('"', '').replace("'", "")
    # treat anything that’s not a number or letter as a space
    rv = "".join(c if c.isalnum() else " " for c in rv)
    # trim multiple spaces to a single space
    rv = re.sub(r"\s{2,}", " ", rv)
    # stem
    rv = " ".join(map(stemmer.stem, rv.split(" ")))
    return rv

print("normalizing queries...")
df['query'] = df['query'].map(normalize)

# Compute query counts
def counts_sorted(df):
    return df.groupby('category', sort=False).count().rename(columns={"query": "count"}).sort_values("count")

df_counts_sorted = counts_sorted(df)

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
rarest, next_rarest = df_counts_sorted.iloc[0], df_counts_sorted.iloc[1]
if rarest.name == root_category_id:
    rarest = next_rarest
print("rolling up categories...")
while rarest.values[0] < min_queries:
    category = rarest.name
    print(f"rolling up {category} (only {rarest.values[0]} queries)...")
    parent = parents_df[parents_df["category"] == category].iloc[0].parent
    df.loc[df["category"] == category, 'category'] = parent
    df_counts_sorted = counts_sorted(df)
    rarest, next_rarest = df_counts_sorted.iloc[0], df_counts_sorted.iloc[1]
    if rarest.name == root_category_id:
        rarest = next_rarest

print("creating labels...")
# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)

# python week3/create_labeled_queries.py --min_queries 1000
# cut -d '_' -f 5 /Users/dwinston/datasets/search_with_ml/labeled_query_data.txt | cut -d ' ' -f 1 | sort | uniq | wc -l
# 312
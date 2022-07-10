Shuffle and set training and test data.
```
shuf labeled_query_data.txt > shuffled_labeled_query_data.txt
head -50000 shuffled_labeled_query_data.txt > queries.train
tail -10000 shuffled_labeled_query_data.txt > queries.test
```
Train and test
```
fasttext supervised -input queries.train -output model_queries
fasttext test model_queries.bin queries.test 1 # R@1 0.53
fasttext test model_queries.bin queries.test 3 # R@3 0.701
fasttext test model_queries.bin queries.test 5 # R@5 0.762
```
Hyperparameter tuning
```
fasttext supervised -input queries.train -output model_queries -lr 0.5 -epoch 25
# test results: R@1 0.567, R@3 0.748, R@5 0.806
fasttext supervised -input queries.train -output model_queries -lr 0.5 -epoch 25 -wordNgrams 2
# test results: R@1 0.565, R@3 0.749, R@5 0.807
# => I'll stick with -lr 0.5 -epoch 25 and without -wordNgrams 2. Uncertain return.
```
Minimum Threshold of 10,000 queries per category:
```
python week3/create_labeled_queries.py --min_queries 10000
cut -d '_' -f 5 labeled_query_data.txt | cut -d ' ' -f 1 | sort | uniq | wc -l
# 40 (was 312 for min_queries==1000)

# Re-evaluate
shuf labeled_query_data.txt > shuffled_labeled_query_data.txt
head -50000 shuffled_labeled_query_data.txt > queries.train
tail -10000 shuffled_labeled_query_data.txt > queries.test
fasttext supervised -input queries.train -output model_queries -lr 0.5 -epoch 25
# test results: R@1 0.7, R@3 0.866, R@5 0.907
```

Remove query normalization to see how much it degrades model accuracy? No thanks. 
Creating labeled queries @ min_queries=1000 takes ~20min 
(Only an additional ~4min for min_queries=10000 though!).

Predictions compared with classifying by eye/hand:

```
 fasttext predict model_queries.bin -
iphone
__label__cat02015 # Movies &amp; TV Shows
lcd tv
__label__abcat0101001 #  All Flat-Panel TVs
ssd
__label__pcmcat209000050007 # iPad
hard drive
__label__pcmcat186100050006 # Portable External Hard Drives
```
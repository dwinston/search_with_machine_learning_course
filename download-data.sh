DATASETS_ROOT="/Users/dwinston/datasets/search_with_ml"

cd $DATASETS_ROOT
# TODO: put in validation checks
#pip install kaggle
echo "Downloading Kaggle"
kaggle competitions download -c acm-sf-chapter-hackathon-big
unzip acm-sf-chapter-hackathon-big.zip
tar -xf product_data.tar.gz
echo "Cleaning up to save space:"
rm acm-sf-chapter-hackathon-big.zip
rm product_data.tar.gz
rm popular_skus.csv
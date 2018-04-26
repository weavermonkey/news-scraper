from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from tqdm import tqdm
from src.utils.add_meta_tags import convert_dict_to_columns
tqdm.pandas()

def assign_sentiment(input_text):
    return SentimentIntensityAnalyzer().polarity_scores(input_text)

def convert_dict_to_columns(input_df, dict_column, prefix=''):
    dict_df = input_df[dict_column].progress_apply(pd.Series)
    dict_df.columns = [prefix + '_' + x for x in dict_df.columns]
    output_df = pd.concat([input_df, dict_df], axis=1).drop(columns=[dict_column])
    return output_df

input_df = pd.read_csv('../../data/tmp/articles/aiooo.csv')
input_df = input_df.fillna(' ')
input_df['meta_title_plus_meta_description'] = input_df['meta__description'].to_string() + input_df['meta__title'].to_string()
input_df['article_sentiment'] = input_df['article_text'].progress_apply(assign_sentiment)

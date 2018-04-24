from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm,tqdm_pandas
import requests

tqdm.pandas()

def return_html_from_url(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    html_content = requests.get(article_url,headers=headers)
    return html_content

input_article_csv = '/home/varun/PycharmProjects/news_scraper/articles_sentiment.csv'
input_df = pd.read_csv(input_article_csv)
input_df['article_html'] = input_df['article_url'].progress_apply(return_html_from_url)
input_df.to_csv('/home/varun/PycharmProjects/news_scraper/articles_with_meta_tags.csv',index=False)
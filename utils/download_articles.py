import os
import newspaper
from newspaper import Config, Article, Source,news_pool
import time
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from utils.read_site_tlds import URLListBuilder


class NewspaperBuilder():
    def __init__(self,site_tld, file_index=str(int(time.time()))):
        self.config_obj = Config()
        self.config_obj.memoize_articles = False
        self.config_obj.keep_article_html = True
        self.config_obj.http_success_only = False
        self.config_obj.MAX_TEXT = 999999
        self.config_obj.verbose = True
        self.file_path = os.path.join(os.path.join(os.getcwd(), 'data/tmp/articles'), file_index + '.csv')
        self.file_write_time = file_index
        self.newspaper = newspaper.build(url=site_tld,config=self.config_obj)

    def article_downloader(self,article_url):
        article_list = []
        article_dict = {'article_url':'','article_html':''}
        article = newspaper.Article(url=article_url, config=self.config_obj)
        try:
            retries = 0
            article.download()
            while article.download_state == 0:
                time.sleep(1)
                retries += 1
                if retries == 5:
                    raise Exception("Couldn't download from URL")
            article.parse()
            article_dict['download_time'] = self.file_write_time
            article_dict['article_url'] = article.url
            article_dict['article_html'] = article.html
            article_dict['article_text'] = article.text
        except Exception as e:
            article_dict['article_url'] = article.url
        article_list.append(article_dict)
        article_df = pd.DataFrame.from_dict([article_dict])
        return article_df


class DataFrameBuilder():
    def __init__(self,article_url):
        article_obj = newspaper.Article(article_url)
        try:
            article_obj.download()
        except Exception as e:
            pass
        movie_dict = {}


class FileWriter():
    def __init__(self,article_obj, file_path='../data/tmp/site_responses/complete_html.csv'):
        try:
            if Path(file_path).exists():
                article_obj.to_csv(file_path, mode='a', index=False,header=False,encoding='utf-8')
            else:
                article_obj.to_csv(file_path,index=False)
                #logging.basicConfig(filename='/tmp/logs/file_writing_logs.log',level=logging.DEBUG)
        except Exception as e:
            print(e)


def start_pipeline():
    for curr_tld in tqdm(URLListBuilder().url_list  ):
        curr_newspaper = NewspaperBuilder(site_tld=curr_tld)
        for curr_article in tqdm(curr_newspaper.newspaper.articles):
            curr_article_df = curr_newspaper.article_downloader(curr_article.url)
            FileWriter(curr_article_df)
            print(curr_article.url)

if __name__ == '__main__':
    start_pipeline()
import pandas as pd
import nltk

class ArticleLoader():
    def __init__(self, file_path='../data/tmp/site_responses/complete_html.csv'):
        self.articles= pd.read_csv(file_path)['article_text'].sample(1).replace('\n',' ',regex=True).tolist()


x = ArticleLoader().articles[0]

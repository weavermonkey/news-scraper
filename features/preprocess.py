import pandas as pd
import contractions


class ArticleLoader():
    def __init__(self, file_path='../data/tmp/articles/wololo.csv'):
        self.articles = pd.read_csv(file_path)['article_text'].replace('\n', ' ', regex=True).tolist()


class Preprocess():
    def __init__(self, article_list):
        try:
            self.contractions_fixed = [contractions.fix(z) for z in [y for y in article_list]]
        except Exception as e:
            print(article_list)

import pandas as pd
import contractions
import nltk



class ArticleLoader():
    def __init__(self, file_path='../data/tmp/articles/wololo.csv'):
        self.articles = pd.read_csv(file_path)['article_text'].sample(5).replace('\n', ' ', regex=True).tolist()


class Preprocess():
    def __init__(self, article_list):
        try:
            self.contractions_fixed = [contractions.fix(z) for z in [y for y in article_list]]
            self.tokens_list = self.article_tokenizer(self.contractions_fixed)
        except Exception as e:
            print(e)
    def article_tokenizer(self,article_list,method='nltk'):
        if method == 'nltk':
            return [ nltk.word_tokenize(x) for x in article_list ]

articles = ArticleLoader().articles
y = Preprocess(articles).article_tokenizer(articles)
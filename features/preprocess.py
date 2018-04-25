import pandas as pd
import contractions
import nltk


class ArticleLoader():
    def __init__(self, file_path='../data/tmp/articles/wololo.csv'):
        self.articles = pd.read_csv(file_path)['article_text'].replace('\n', ' ', regex=True).tolist()


class Preprocess():
    def __init__(self, article_list):
        try:
            self.contractions_fixed = [contractions.fix(z) for z in [y for y in article_list]]
            self.tokens_list = self.article_tokenizer(self.contractions_fixed)
        except Exception as e:
            print(e)

    def article_tokenizer(self, article_list, method='nltk'):
        tokens = []
        if method == 'nltk':
            for curr_text in article_list:
                article_tokens = nltk.word_tokenize(curr_text)
                tokens.append(article_tokens)
        return tokens


articles = ArticleLoader().articles

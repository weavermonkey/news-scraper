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
        stop_words = nltk.corpus.stopwords.words('english')
        stopped_tokens_removed = []
        if method == 'nltk':
            for curr_text in article_list:
                tokens = nltk.word_tokenize(curr_text)
                y = [token for token in tokens if not token in stop_words]
                stopped_tokens_removed.append(y)
        return stopped_tokens_removed

articles = ArticleLoader().articles
y = Preprocess(articles).article_tokenizer(articles)
print(articles[2],'\n',y[2])

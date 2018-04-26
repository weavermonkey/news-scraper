import pandas as pd
import contractions
import nltk
from nltk.corpus import stopwords

class ArticleLoader():
    def __init__(self, file_path='../data/tmp/articles/wololo.csv'):
        self.articles = pd.read_csv(file_path)['article_text'].replace('\n', ' ', regex=True).tolist()


class Preprocess():
    '''
    def __init__(self, article_list):
        try:
            self.contractions_fixed = [contractions.fix(z) for z in [y for y in article_list]]
            self.tokens_list = self.article_tokenizer(self.contractions_fixed)
        except Exception as e:
            print(e)
    '''

    def article_tokenizer(self, article_list, method='nltk',remove_stop_words=False):
        tokens = []
        if remove_stop_words:
            for curr_text in article_list:
                curr_tokens = nltk.word_tokenize( curr_text )
                stop_words = stopwords.words('english')
                tokens.append( [x for x in curr_tokens if x.lower() not in stop_words ])
        else:
            for curr_text in article_list:
                tokens =  [ nltk.word_tokenize(curr_text) for curr_text in article_list ]
        return tokens


article_list = ["A Human machine interface for lab abc computer applications","A survey of user opinion of computer system response time", "The EPS user interface management system","System and human system engineering testing of EPS","Relation of user perceived response time to error measurement"]
y = Preprocess().article_tokenizer(article_list)
print(y)
y = Preprocess().article_tokenizer(article_list,remove_stop_words=True)
print(y)
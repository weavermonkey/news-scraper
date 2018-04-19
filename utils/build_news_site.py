import os
import time

import newspaper


class NewspaperBuilder():
    def __init__(self, site_tld, file_index=str(int(time.time()))):
        self.newspaper = newspaper.build(site_tld, memoize_articles=False)
        self.file_name = os.path.join(os.path.join(os.getcwd(), 'data/tmp/articles'), file_index + '.csv')


x = NewspaperBuilder(site_tld='https://www.thequint.com/')


def download_articles():
    for curr_article in x.newspaper.articles:
        curr_article.download()
        print(curr_article.html)
        time.sleep(10)


download_articles()

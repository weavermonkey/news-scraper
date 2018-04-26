import pandas as pd
from bs4 import BeautifulSoup
from tldextract import extract as tld_extract
from tqdm import tqdm, tqdm_pandas

tqdm.pandas()


def fetch_meta_attributes(input_html):
    meta_content = {}
    soup_obj = BeautifulSoup(input_html, 'lxml')
    site_lookup_dict = {
        'thequint': [{'property': 'og:title'}, {'name': ['keywords', 'title', 'description']}],
        'indiatimes': [{'name': ['keywords', 'title', 'description']}, {'property': 'og:title'}],
        'afternoondc': [{'property': 'og:title'}, {'name': ['keywords', 'title', 'description']}],
        'dailyo': [{'property': 'og:title'}, {'name': ['keywords', 'title', 'description']}],
        'qz': [{'property': 'og:title'}, {'name': ['title', 'news_keywords', 'description']}],
        'scroll': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'dnaindia': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'firstpost': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'thehansindia': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'thehindu': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'thehindubusinessline': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'hindustantimes': [{'property': ['og:title', 'og:description']}, {'name': 'keywords'}],
        'indianexpress': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'mid-day': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'livemint': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'orissapost': [{'property': ['og:title', 'og:description']}, {'name': ['title', 'keywords', 'description']}],
        'dailypioneer': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'sundayguardianlive': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],  # NO keywords
        'thestatesman': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'telegraphindia': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],  # NO keywords
        'tribuneindia': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'kashmirreader': [{'property': ['og:title', 'og:description']}, {'name': ['title', 'keywords', 'description']}],
        # NO keywords
        'asianage': [{'property': ['og:title', 'og:description']}, {'name': 'Keywords'}],
        'bangaloremirror': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'newindianexpress': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'deccanchronicle': [{'property': ['og:title', 'og:description']}, {'name': ['Keywords']}],
        'deccanherald': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'economictimes': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'financialexpress': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'mydigitalfc': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'afternoondc': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'business-standard': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'speakingtree': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'cricbuzz': [{'property': 'og:title'}, {'name': ['title', 'keywords', 'description']}],
        'indiatimes': [{'name': ['keywords', 'title', 'description']}, {'property': 'og:title'}],
        'femina': [{'name': ['keywords', 'title', 'description']}, {'property': 'og:title'}]

    }
    try:
        input_url = soup_obj.find('meta', {'property': 'og:url'}).get('content')
        for curr_attr_map in site_lookup_dict[tld_extract(input_url).domain]:
            if type(curr_attr_map) is dict:
                meta_map = curr_attr_map
            else:
                meta_map = {curr_attr_map: site_lookup_dict[tld_extract(input_url).domain][curr_attr_map]}
            meta_tags = soup_obj.find_all('meta', meta_map)
            for curr_tag in meta_tags:
                tag_content = curr_tag.get('content')
                if curr_tag.get('name'):
                    meta_content[curr_tag.get('name').lower()] = tag_content
                else:
                    meta_content[curr_tag.get('property').replace('og:', '').lower()] = tag_content
    except (KeyError, TypeError, AttributeError, UnboundLocalError) as e:
        pass
    return meta_content


def convert_dict_to_columns(input_df, dict_column, prefix=''):
    dict_df = input_df[dict_column].apply(pd.Series)
    dict_df.columns = [prefix + '_' + x for x in dict_df.columns]
    output_df = pd.concat([input_df, dict_df], axis=1).drop(columns=[dict_column])
    return output_df


def file_writer():
    input_df = pd.read_csv('../../data/tmp/site_responses/complete_html_2.csv')
    input_df['article_len'] = input_df['article_text'].str.len()
    input_df = input_df[input_df['article_html'].notnull()].drop(columns=['download_time'])
    input_df['meta_content'] = input_df['article_html'].progress_apply(fetch_meta_attributes)
    input_df = input_df.drop(columns=['article_html'])
    columns = ['article_url', 'article_text', 'meta_content','article_len']
    input_df = input_df[columns]
    output_df = convert_dict_to_columns(input_df, dict_column='meta_content', prefix='meta')
    output_df = output_df[output_df['article_text'].notnull()]
    output_df['article_text'] = output_df['article_text'].replace('\n',' ',regex=True)
    output_df.to_csv('../../data/tmp/articles/meta_content.csv', index=False)


if __name__ == '__main__':
    file_writer()
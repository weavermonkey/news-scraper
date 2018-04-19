import json


class URLListBuilder():
    def __init__(self, config_source='local_json'):
        self.functions = {'local_json': self.url_list_from_json}
        self.url_list = self.functions[config_source]()

    def url_list_from_json(self):
        sites_json = json.load(open('../config/news_sites.json'))
        url_list = ([y['website_tld'] for y in [x for x in sites_json['site_config']]])
        return url_list

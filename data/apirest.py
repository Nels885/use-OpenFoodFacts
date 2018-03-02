"""
API OpenfoodFacts management module
"""

import requests

from data.glob import Glob


class Apirest:

    def __init__(self, log):
        """
        ## Initialize Class Apirest ##
        :param log: logging module
        """
        self.log = log
        self.tag_0 = "&tagtype_0={}&tag_contains_0={}&tag_0={}".format(
            Glob.infoApi['tagtype_0'],
            Glob.infoApi['tag_contains_0'],
            Glob.infoApi['tag_0'])
        self.tag_1 = "&tagtype_1={}&tag_contains_1={}&tag_1=".format(
            Glob.infoApi['tagtype_1'],
            Glob.infoApi['tag_contains_1'])
        self.cmdRequest = "{}&action={}&sort_by={}&page_size={}&json={}".format(
            Glob.infoApi['https'],
            Glob.infoApi['action'],
            Glob.infoApi['sort_by'],
            Glob.infoApi['page_size'],
            Glob.infoApi['json'])
        self.data = 'products'

    def get_request(self, tag):
        """
        ## Execute API request ##
            :param tag: value of the reseach
            :return: data in json format
        """
        r = requests.get("{}{}{}{}".format(self.cmdRequest, self.tag_0, self.tag_1, tag))
        self.log.info("# Status Code: {} #".format(r.status_code))
        self.log.info("# Headers: {} #\n".format(r.headers['content-type']))
        return r.json()[self.data]



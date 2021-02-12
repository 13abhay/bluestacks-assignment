from googlesearch import search

import os,logging

logger = logging.getLogger(os.path.basename(__file__))


class GoogleSearch:

    @classmethod
    def search(cls, query, num=5):
        """
        Search google.
        Reference : https://www.geeksforgeeks.org/performing-google-search-using-python-code/
        """
        try:
            # searching for query on google search.
            results = search(query, tld='co.in', lang='en', num=num, start=0, stop=num, pause=2.0)
            returnable_string = ""

            for ind,result in enumerate(results):
                returnable_string = returnable_string + str(ind+1) + ". " + result + "\n "
            
            return returnable_string
        except Exception as e:
            logger.info("Search Error : query:{} with error : {}".format(query, str(e)))
            raise e
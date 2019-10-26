import json
import urllib.request
import urllib.parse


class WalmartApi:
    baseUrl = "https://grocery.walmart.com/v4/api/products"

    def buildSearchUrl(self, search_query: str, store_id: str = 5609) -> str:
        #Temporary store_id
        query_parameters = [
            ('storeId', store_id),
            ('query', search_query),
            ('count', 60),
            ('page', 1),
            ('offset', 0)
        ]

        return WalmartApi.baseUrl + '/search?' + urllib.parse.urlencode(query_parameters)

    def getResult(self, url: str) -> dict:
        response = None
        
        try:
            response = urllib.request.urlopen(url)
            json_text = response.read().decode(encoding = 'utf-8')
            
            return json.loads(json_text)
        
        finally:
            if response != None:
                response.close()

    def getNameImagePrice(self, results: dict):
        resultProducts = results['products'][0]

        

        print(resultProducts)

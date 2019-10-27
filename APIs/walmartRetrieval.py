import json
import urllib.request
import urllib.parse
import re
import pint


class ProductDetail:
    def __init__(self, name: str, imageUrl: str, price: float, quant: int, quantType: str):
        self.name = name
        self.imageUrl = imageUrl
        self.price = price
        self.amount = quant
        self.unit = quantType

    def getName(self):
        return self.name

    def getImageUrl(self):
        return self.imageUrl

    def getPrice(self):
        return self.price

    def getQuant(self):
        # Returns quantity amount like 16
        return self.amount

    def getQuantType(self):
        # Returns quantity type like fl oz
        return self.unit


class WalmartApi:
    def __init__(self, ureg):
        self.ureg = ureg

    baseUrl = "https://grocery.walmart.com/v4/api/products"

    def query_search(self, search_query: str) -> ProductDetail:
        return self.getNameImagePriceQuant(self.getResult(self.buildSearchUrl(search_query)), search_query)

    def buildSearchUrl(self, search_query: str, store_id: str = 5609) -> str:
        # Temporary store_id
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
            json_text = response.read().decode(encoding='utf-8')

            return json.loads(json_text)

        finally:
            if response != None:
                response.close()


    def getNameImagePriceQuant(self, results: dict, search_query) -> ProductDetail:
        possibleQuants = [
            ' each',
            ' bunch',
            ' count',
            ' fl oz',
            ' fluid ounce',
            ' oz',
            ' gal',
            ' lb',
            ' bag'
        ]

        prodResults = results['products'][0]

        name = search_query
        img = prodResults['basic']['image']['thumbnail']
        price = prodResults['store']['price']['list']
        quant = ""
        quantType = ""

        productUrl = prodResults['basic']['name'].lower()

        # Attempts to isolate the quantity and quantity type in the name
        for qType in possibleQuants:
            if qType in productUrl:
                qLen = len(qType)
                qIndex = productUrl.find(qType)
                quant = productUrl[(qIndex - 5):(qIndex + qLen)].strip()
                quantType = qType
                break

        # Special case if the quantity is each
        if (quantType != " each"):
            match = re.search(r"\d", quant)

            if match.start() is not None:
                quant = quant[int(match.start()):]

        elif (quantType == " each"):
            quant = "1 " + 'count'

        quant = quant.split()
        amount = int(quant[0])
        unit = quant[1]
        if unit == 'oz':
            unit = 'floz'

        if unit == 'bunch':
            unit = 'count'
            amount = 3
        elif unit == 'bag':
            unit = 'count'
            amount = 15
        elif unit == 'count':
            pass
        #else:
        #    unit = self.ureg.parse_expression(unit)

        return ProductDetail(name, img, price, amount, unit)

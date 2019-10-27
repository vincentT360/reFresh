import urllib.request
import urllib.parse
import re
import pint
import json


class ProductDetail:
    def __init__(self, name: str, imageUrl: str, price: float, quant: float, quantType: str):
        self.name = name
        self.imageUrl = imageUrl
        self.price = price
        self.quant = quant
        self.quantType = quantType
    

    def getName(self):
        return self.name

    def getImageUrl(self):
        return self.imageUrl
    

    def getPrice(self):
        return self.price
    

    def getQuant(self):
        #Returns quantity amount like 16
        # Returns quantity amount like 16
        return self.quant
    

    def getQuantType(self):
        #Returns quantity type like fl oz
        # Returns quantity type like fl oz
        return self.quantType


class WalmartApi:
    def __init__(self, ureg):
        self.ureg = ureg

    baseUrl = "https://grocery.walmart.com/v4/api/products"

    def query_search(self, search_query: str) -> ProductDetail:
        return self.getNameImagePriceQuant(self.getResult(self.buildSearchUrl(search_query)))

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

    def getNameImagePriceQuant(self, results: dict) -> ProductDetail:

        possibleQuants = [
            ' each',
            ' bunch',
            ' count',
            ' fl oz',
            ' fluid ounce',
            ' oz',
            ' gal',
            ' lb',
            ' bag',
            '-ounce',
            ' pint'
            ' gallon'
            ' ounce'
        ]

        prodResults = results['products'][0]

        name = prodResults['basic']['name']
        img = prodResults['basic']['image']['thumbnail']
        price = prodResults['store']['price']['list']
        quant = ""
        quantType = ""

        productUrl = prodResults['basic']['name'].lower()

        #Attempts to isolate the quantity and quantity type in the name
        # Attempts to isolate the quantity and quantity type in the name
        for qType in possibleQuants:
            if qType in productUrl:
                if(qType == "-ounce"):
                    qType = " oz"
                    productUrl=productUrl.replace("-ounce", " oz")
                qLen = len(qType)
                qIndex = productUrl.find(qType)
                quant = productUrl[(qIndex-5):(qIndex+qLen)].strip()
                quantType = qType
                break

        #Special case if the quantity is each or bunch
        if(quantType != " each" and quantType != " bunch"):

            match = re.search(r"\d", quant)

            if match.start() is not None:
                quant = quant[int(match.start()):]

        elif(quantType == " each"):
            quant = quant[quant.find("each"):]
            quant = "1 " + quant

        elif(quantType == " bunch"):
            quant = "4 count"

        quant = quant.split()
        product = ProductDetail(name, img, price, float(quant[0]), quant[1])

        return product 

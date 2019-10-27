import json
import urllib.parse
import urllib.request
import requests

def get_complex_search_url(ingredients: [str], allergies:[str]) ->str:
    base_url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=bd94a1ee3f1c4f4ba21b570dac65d57f&number=2&'
    parameters = ['includeIngredients','intolerances']
    url =base_url + parameters[0] + '='
    for ingredient in ingredients:
        url = url+','+ ingredient
    url = url + '&'+parameters[1]+'='
    for allergy in allergies:
        url = url+','+allergy 
    return url

def get_ingredient_search_url(ingredients:[str]) -> str:
    base_url = 'https://api.spoonacular.com/recipes/findByIngredients?apiKey=bd94a1ee3f1c4f4ba21b570dac65d57f&number=2&ingredients='
    url = base_url+ ingredients[0]
    for ingredient in ingredients[1::]:
        url = url+',+'+ ingredient
    print(requests.get(url).json())
    return url

def get_recipe_info_url(recipe_id:str) -> str:
    return 'https://api.spoonacular.com/recipes/'+recipe_id+'/information?apiKey=bd94a1ee3f1c4f4ba21b570dac65d57f&'

def get_data(url: str) -> dict:
    '''
    Takes a URL and returns a Python dictionary representing the
    parsed JSON response.
    '''
    response = None

    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)

    finally:
        if response != None:
            response.close()

def complex_search_results(search_results:dict)->(str,dict):
    total_results = search_results['totalResults']
    results = dict()
    for result in search_results['results']:
        results[result['id']] = [result['image'],result['title']]
    return (total_results, results)

def ingredient_search_results(search_results:dict)->dict:
    results = dict()
    for result in search_results:
        results[search_result['id']] = [search_result['image'],search_result['title'],search_result['missedIngredients'],search_result['unusedIngredients'],search_result['usedIngredients']]
    return total_results, results

if __name__ == "__main__":
    get_ingredient_search_url(['fettucine','tomato'])
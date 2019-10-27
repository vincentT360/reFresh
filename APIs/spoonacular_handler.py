import os
import requests


class Spoonacular:
    def __init__(self):
        self._api_key = os.environ['SP_KEY']

    def search_recipes(self, query, limit=3):
        url = 'https://api.spoonacular.com/recipes/search'
        body = {
            'apiKey': self._api_key,
            'number': limit,
            'query': query
        }
        response = requests.get(url, params=body).json()
        return [
            Meal(meal['title'], meal['id'], 'https://spoonacular.com/recipeImages/' + meal['image'],
                 self.find_by_id(meal['id']), [], prebuilt=True)
            for meal in
            response['results']]

    def find_by_id(self, id):
        url = f'https://api.spoonacular.com/recipes/{id}/ingredientWidget.json'
        body = {
            'apiKey': self._api_key
        }
        response = requests.get(url, params=body).json()
        return {ing['name']: Ingredient(ing['name'], -1, ing['image'], ing['amount']['us']['unit'],
                                        ing['amount']['us']['value'], ing['name']) for ing in
                response['ingredients']}

    def find_by_ingredients(self, ingredients: [str], limit=3):
        url = 'https://api.spoonacular.com/recipes/findByIngredients'
        body = {
            'apiKey': self._api_key,
            'number': limit,
            'ingredients': ",+".join(ingredients)
        }
        response = requests.get(url=url, params=body).json()
        return self._parse_response_by_ingredients(response)

    def _parse_response_by_ingredients(self, response):
        return [Meal(meal['title'], meal['id'], meal['image'], meal['missedIngredients'], meal['usedIngredients']) for
                meal in response]


class Meal:
    def __init__(self, title, id, image, missedIngredients, usedIngredients, prebuilt=False):
        self.title = title
        self.sp_id = id
        self.image = image
        if prebuilt:
            self.ingredients = missedIngredients
        else:
            self.ingredients = {ing['name']:
                                    Ingredient(ing['name'], ing['id'], ing['image'], ing['unit'], ing['amount'],
                                               ing['original']) for ing in
                                missedIngredients + usedIngredients}


class Ingredient:

    def __init__(self, name, id, image, unit, amount, original):
        self.name = name
        self.sp_id = id
        self.image = image
        self.unit = unit
        self.amount = amount
        self.full_title = original

    def __str__(self):
        return self.full_title


if __name__ == '__main__':
    Spoonacular().search_recipes('pizza')

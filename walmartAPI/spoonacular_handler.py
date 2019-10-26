import os
import requests
import pint


class Spoonacular:
    def __init__(self):
        self._api_key = os.environ['SP_KEY']

    def find_by_ingredients(self, limit: int, ingredients: [str]):
        url = 'https://api.spoonacular.com/recipes/findByIngredients'
        body = {
            'apiKey': self._api_key,
            'number': limit,
            'ingredients': ",+".join(ingredients)
        }
        response = requests.get(url=url, params=body).json()
        return [Meal(meal['title'], meal['id'], meal['image'], meal['missedIngredients'], meal['usedIngredients']) for
                meal in response]


class Meal:
    def __init__(self, title, id, image, missedIngredients, usedIngredients):
        self.title = title
        self.sp_id = id
        self.image = image
        self.ingredients = {
            Ingredient(ing['name'], ing['id'], ing['image'], ing['unit'], ing['amount'], ing['original']) for ing in
            missedIngredients + usedIngredients}


class Ingredient:
    ureg = pint.UnitRegistry()

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
    x = Spoonacular().find_by_ingredients(2, ['chicken', 'peas'])

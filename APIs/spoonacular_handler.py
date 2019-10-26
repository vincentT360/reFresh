import os
import requests
import pint

import APIs.walmartRetrieval as wallAPI


class Spoonacular:
    def __init__(self, ureg):
        self._api_key = os.environ['SP_KEY']
        self.ureg = ureg

    def find_by_ingredients(self, ingredients: [str], limit=2):
        url = 'https://api.spoonacular.com/recipes/findByIngredients'
        body = {
            'apiKey': self._api_key,
            'number': limit,
            'ingredients': ",+".join(ingredients)
        }
        response = requests.get(url=url, params=body).json()
        return self._parse_response_by_ingredients(response)

    def _parse_response_by_ingredients(self, response):
        return [Meal(meal['title'], meal['id'], meal['image'], meal['missedIngredients'], meal['usedIngredients'],
                     self.ureg) for meal in response]


class Meal:
    def __init__(self, title, id, image, missedIngredients, usedIngredients, ureg):
        self.ureg = ureg
        self.title = title
        self.sp_id = id
        self.image = image
        self.ingredients = {ing['name']:
                                Ingredient(ing['name'], ing['id'], ing['image'], ing['unit'], ing['amount'],
                                           ing['original'], self.ureg) for ing in
                            missedIngredients + usedIngredients}

    def __sub__(self, right):
        if type(right) is wallAPI.ProductDetail:
            return self.ingredients[right.name] - right
        else:
            raise


class Ingredient:

    def __init__(self, name, id, image, unit, amount, original, ureg):
        self.ureg = ureg
        self.name = name
        self.sp_id = id
        self.image = image
        try:
            if any((u in unit) for u in ('serving', 'inch', 'large', 'medium')):
                self.unit = 'count'
            else:
                self.unit = self.ureg.parse_expression(unit)
        except pint.errors.UndefinedUnitError:
            self.unit = 'count'
        self.amount = amount
        self.full_title = original

    def __str__(self):
        return self.full_title

    def __sub__(self, right):
        if type(right) in (wallAPI.ProductDetail, Ingredient):
            runit = self.unit if self.unit != 'count' else 1
            lunit = right.unit if right.unit != 'count' else 1
            amount = self.amount * lunit - right.amount * runit

            return Ingredient(self.name, self.sp_id, self.image, str(amount / amount), amount, self.full_title, self.ureg)
        else:
            raise TypeError(f'Cannot subtract {type(right)} from Ingredient.')

    def __neg__(self):
        return Ingredient(self.name, self.sp_id, self.image, str(self.unit), -self.amount, self.full_title, self.ureg)


if __name__ == '__main__':
    reg = pint.UnitRegistry()
    x = Spoonacular(reg)._parse_response_by_ingredients([{'id': 1105658,
                                                       'title': 'Instant Pot Apricot Chicken Recipe with Rice',
                                                       'image': 'https://spoonacular.com/recipeImages/1105658-312x231.jpg',
                                                       'imageType': 'jpg', 'usedIngredientCount': 2,
                                                       'missedIngredientCount': 3, 'missedIngredients': [
            {'id': 9156, 'amount': 1.0, 'unit': '', 'unitLong': '', 'unitShort': '', 'aisle': 'Produce',
             'name': 'lemon zest', 'original': '1 lemon, zest and juice 2 Tbsp parsley, chopped',
             'originalString': '1 lemon, zest and juice 2 Tbsp parsley, chopped',
             'originalName': 'lemon, zest and juice 2 Tbsp parsley, chopped', 'metaInformation': ['chopped'],
             'image': 'https://spoonacular.com/cdn/ingredients_100x100/zest-lemon.jpg'},
            {'id': 10220444, 'amount': 1.0, 'unit': 'cup', 'unitLong': 'cup', 'unitShort': 'cup',
             'aisle': 'Pasta and Rice', 'name': 'white rice',
             'original': '1 cup long-grain white rice, uncooked ½ cup cold water ½ cup chicken broth',
             'originalString': '1 cup long-grain white rice, uncooked ½ cup cold water ½ cup chicken broth',
             'originalName': 'long-grain white rice, uncooked ½ cup cold water ½ cup chicken broth',
             'metaInformation': ['long-grain', 'white', 'cold', 'uncooked'],
             'image': 'https://spoonacular.com/cdn/ingredients_100x100/rice-white-long-grain-or-basmatii-cooked.jpg'},
            {'id': 20048, 'amount': 1.0, 'unit': 'serving', 'unitLong': 'serving', 'unitShort': 'serving',
             'aisle': 'Pasta and Rice', 'name': 'quick-cooking white rice', 'original': 'Add to Rice After Cooking',
             'originalString': 'Add to Rice After Cooking', 'originalName': 'Add to Rice After Cooking',
             'metaInformation': [],
             'image': 'https://spoonacular.com/cdn/ingredients_100x100/uncooked-white-rice.png'}], 'usedIngredients': [
            {'id': 5006, 'amount': 1.0, 'unit': 'serving', 'unitLong': 'serving', 'unitShort': 'serving',
             'aisle': 'Meat', 'name': 'chicken', 'original': 'Add to Chicken After Cooking',
             'originalString': 'Add to Chicken After Cooking', 'originalName': 'Add to Chicken After Cooking',
             'metaInformation': [], 'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg'},
            {'id': 11304, 'amount': 0.5, 'unit': 'cup', 'unitLong': 'cups', 'unitShort': 'cup', 'aisle': 'Produce',
             'name': 'peas', 'original': '½ cup frozen peas, thawed salt, to taste',
             'originalString': '½ cup frozen peas, thawed salt, to taste',
             'originalName': 'frozen peas, thawed salt, to taste', 'metaInformation': ['frozen', 'thawed', 'to taste'],
             'extendedName': 'frozen peas', 'image': 'https://spoonacular.com/cdn/ingredients_100x100/peas.jpg'}],
                                                       'unusedIngredients': [], 'likes': 1},
                                                      {'id': 469895, 'title': "Gram's Chicken Pot Pie",
                                                       'image': 'https://spoonacular.com/recipeImages/469895-312x231.jpg',
                                                       'imageType': 'jpg', 'usedIngredientCount': 2,
                                                       'missedIngredientCount': 3, 'missedIngredients': [
                                                          {'id': 1006080, 'amount': 1.0, 'unit': 'teaspoon',
                                                           'unitLong': 'teaspoon', 'unitShort': 'tsp',
                                                           'aisle': 'Canned and Jarred',
                                                           'name': 'chicken bouillon granules',
                                                           'original': '1 teaspoon chicken bouillon granules',
                                                           'originalString': '1 teaspoon chicken bouillon granules',
                                                           'originalName': 'chicken bouillon granules',
                                                           'metaInformation': [],
                                                           'image': 'https://spoonacular.com/cdn/ingredients_100x100/stock-powder.png'},
                                                          {'id': 6147, 'amount': 10.75, 'unit': 'ounce',
                                                           'unitLong': 'ounces', 'unitShort': 'oz',
                                                           'aisle': 'Canned and Jarred',
                                                           'name': 'condensed cream of mushroom soup',
                                                           'original': '1 (10.75 ounce) can condensed cream of mushroom soup',
                                                           'originalString': '1 (10.75 ounce) can condensed cream of mushroom soup',
                                                           'originalName': 'condensed cream of mushroom soup',
                                                           'metaInformation': ['canned'],
                                                           'extendedName': 'canned condensed cream of mushroom soup',
                                                           'image': 'https://spoonacular.com/cdn/ingredients_100x100/cream-of-mushroom-soup.png'},
                                                          {'id': 18945, 'amount': 2.0, 'unit': '9-inch',
                                                           'unitLong': '9-inchs', 'unitShort': '9-inch',
                                                           'aisle': 'Refrigerated;Frozen',
                                                           'name': 'deep dish pie crusts',
                                                           'original': '2 (9 inch) deep dish frozen pie crusts, thawed',
                                                           'originalString': '2 (9 inch) deep dish frozen pie crusts, thawed',
                                                           'originalName': '(9 inch) deep dish frozen pie crusts, thawed',
                                                           'metaInformation': ['frozen', 'thawed', '()'],
                                                           'extendedName': 'frozen deep dish pie crusts',
                                                           'image': 'https://spoonacular.com/cdn/ingredients_100x100/pie-crust.jpg'}],
                                                       'usedIngredients': [
                                                           {'id': 11304, 'amount': 10.0, 'unit': 'ounce',
                                                            'unitLong': 'ounces', 'unitShort': 'oz', 'aisle': 'Produce',
                                                            'name': 'peas',
                                                            'original': '1 (10 ounce) package frozen green peas, thawed',
                                                            'originalString': '1 (10 ounce) package frozen green peas, thawed',
                                                            'originalName': 'package frozen green peas, thawed',
                                                            'metaInformation': ['green', 'frozen', 'thawed'],
                                                            'extendedName': 'frozen green peas',
                                                            'image': 'https://spoonacular.com/cdn/ingredients_100x100/peas.jpg'},
                                                           {'id': 5006, 'amount': 2.0, 'unit': 'pound',
                                                            'unitLong': 'pounds', 'unitShort': 'lb', 'aisle': 'Meat',
                                                            'name': 'whole chicken',
                                                            'original': '1 (2 to 3 pound) whole chicken',
                                                            'originalString': '1 (2 to 3 pound) whole chicken',
                                                            'originalName': 'whole chicken',
                                                            'metaInformation': ['whole'],
                                                            'image': 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg'}],
                                                       'unusedIngredients': [], 'likes': 0}])
    print((x[0] - wallAPI.WalmartApi(reg).query_search('white rice')).amount)


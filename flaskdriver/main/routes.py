from flask import render_template, request, Blueprint, redirect, url_for
from flaskdriver import db
from flaskdriver.models import Ingredient, IngredientProduct, Meal, MealPlan
from flaskdriver.forms import AddIngredientForm, ChooseRecipeForm, SearchRecipeForm
from APIs.walmartRetrieval import WalmartApi
from APIs.spoonacular_handler import Spoonacular
import pint

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    title = "Home"
    return render_template("home.html", title=title)

@main.route("/pick-ingredients", methods=['GET', 'POST'])
def pick_ingredients():
    title = "Pick the groceries you want to get"
    form = AddIngredientForm()
    if form.validate_on_submit():
        new_item = Ingredient(name=form.name.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.pick_ingredients'))

    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    return render_template("pick_ingredients.html", title=title, ingredients=ingredients, form=form)

@main.route("/search-recipes", methods=['GET', 'POST'])
def search_for_recipes():
    title = "Search for a recipe"
    form = SearchRecipeForm()
    if form.validate_on_submit():
        return redirect(url_for('main.get_recipes_from_search', recipes=form.name.data))
    return render_template("search_for_recipes.html", title=title, form=form)

@main.route("/recipes-from-search/<recipes>", methods=['GET', 'POST'])
def get_recipes_from_search(recipes):
    form = ChooseRecipeForm()
    title = "Choose recipes"
    reg = pint.UnitRegistry()
    spoonacular = Spoonacular(reg)
    recipes = spoonacular.search_recipes(recipes)
    form.select.choices = [(recipe.sp_id, recipe.title) for recipe in recipes]

    if form.validate_on_submit():
        chosen_recipe = {recipe.sp_id : recipe for recipe in recipes}[form.select.data]
        meal_plan = MealPlan()
        db.session.add(meal_plan)
        db.session.commit()
        new_meal = Meal(mealplan=meal_plan)
        db.session.add(new_meal)
        db.session.commit()
        for v in chosen_recipe.ingredients.values():
            new_ingredient = IngredientProduct(name=v.name, image_url=v.image, price=0, quantity=v.amount, quantity_type=str(v.unit), meal=new_meal)
            db.session.add(new_ingredient)
            db.session.commit()
        return redirect(url_for('main.get_products'))
    return render_template("recipes.html", title=title, recipes=recipes, form=form) #finish this

@main.route("/recipes-from-ingredients", methods=['GET', 'POST'])
def get_recipes_from_ingredients():
    form = ChooseRecipeForm()
    title = "Choose recipes"
    ingredients = [ingredient.name for ingredient in Ingredient.query.order_by(Ingredient.name).all()]
    reg = pint.UnitRegistry()
    spoonacular = Spoonacular(reg)
    recipes = spoonacular.find_by_ingredients(ingredients)
    form.select.choices = [(recipe.sp_id, recipe.title) for recipe in recipes]

    if form.validate_on_submit():
        chosen_recipe = {recipe.sp_id : recipe for recipe in recipes}[form.select.data]
        meal_plan = MealPlan()
        db.session.add(meal_plan)
        db.session.commit()
        new_meal = Meal(mealplan=meal_plan)
        db.session.add(new_meal)
        db.session.commit()
        for v in chosen_recipe.ingredients.values():
            new_ingredient = IngredientProduct(name=v.name, image_url=v.image, price=0, quantity=v.amount, quantity_type=str(v.unit), meal=new_meal)
            db.session.add(new_ingredient)
            db.session.commit()
        return redirect(url_for('main.get_products'))
    
    return render_template("recipes.html", title=title, recipes=recipes, form=form)

@main.route("/products")
def get_products():
    title = "Your Products"
    product_multiplier_dict = {}
    product_multiplier = 1
    #Focus on IngredientProduct (ingredients from recipe)
    #Get name and put into walmartHandler
    #From walmart handler figure out if quantity sold from walmart is enough
    #If enough then change quantity to leftover quantity
    #If not enough then change price to total for buying x quantities, then change leftover quantity
    ureg = pint.UnitRegistry
    walmart = WalmartApi(ureg)
    ingredients = IngredientProduct.query.options(db.joinedload_all('*')).all()

    try:
        db.session.query(IngredientProduct).delete()
        db.session.commit()
    except:
        db.session.rollback()
    

    for i in ingredients:
        product_multiplier = 1
        walmartItem = walmart.query_search(i.name)
        if(walmartItem.getQuant() >= i.quantity):
            i.quantity = walmartItem.getQuant()
            #New price when we buy 1 item
            i.price = walmartItem.getPrice()
        elif(walmartItem.getQuant() < i.quantity):
            base_quant = walmartItem.getQuant()
            base_price = walmartItem.getPrice()
            #While walmart total quant is less than needed
            #Add more
            while(walmartItem.getQuant() < i.quantity):
                product_multiplier += 1
                walmartItem.price = walmartItem.price + base_price
                walmartItem.amount = walmartItem.amount + base_quant
            i.quantity = walmartItem.getQuant()
            i.price = walmartItem.getPrice()
        new_ingredient = IngredientProduct(name=i.name, image_url=i.image_url, price=i.price, quantity=i.quantity, quantity_type=i.quantity_type, meal=i.meal)
        db.session.add(new_ingredient)
        db.session.commit()
        product_multiplier_dict[i.name] = product_multiplier

    ingredients = IngredientProduct.query.all()

    return render_template("get_products.html", title=title, ingredients=ingredients, product_multiplier_dict=product_multiplier_dict)
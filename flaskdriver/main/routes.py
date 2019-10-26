from flask import render_template, request, Blueprint, redirect, url_for
from flaskdriver import db
from flaskdriver.models import Ingredient, IngredientProduct
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

@main.route("/search-recipes")
def search_for_recipes():
    title = "Search for a recipe"
    form = SearchRecipeForm()
    if form.validate_on_submit():
        reg = pint.UnitRegistry()
        spoonacular = Spoonacular(reg)
        recipes = None
        return redirect(url_for('main.get_recipes', recipes=recipes))

    
    return render_template("search_for_recipes.html", title=title, form=form)

@main.route("/recipes-from-search", methods=['GET', 'POST'])
def get_recipes_from_search(recipes):
    form = ChooseRecipeForm()
    title = "Choose recipes"
    form.select.choices = [(recipe.sp_id, recipe.title) for recipe in recipes]

    if form.validate_on_submit():
        chosen_recipe = {recipe.sp_id : recipe for recipe in recipes}[form.select.data]
        for v in chosen_recipe.ingredients.values():
            new_ingredient = IngredientProduct(name=v.name, image_url=v.image, price=0, quantity=v.amount, quantity_type=str(v.unit))
            db.session.add(new_ingredient)
            db.session.commit()
        redirect(url_for('main.get_products'))
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
        for v in chosen_recipe.ingredients.values():
            new_ingredient = IngredientProduct(name=v.name, image_url=v.image, price=0, quantity=v.amount, quantity_type=str(v.unit))
            db.session.add(new_ingredient)
            db.session.commit()
        return redirect(url_for('main.get_products'))
    
    return render_template("recipes.html", title=title, recipes=recipes, form=form)

@main.route("/products")
def get_products():
    return render_template("get_products.html")
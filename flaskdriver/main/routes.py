from flask import render_template, request, Blueprint, redirect, url_for
from flaskdriver import db
from flaskdriver.models import Ingredient
from flaskdriver.forms import AddIngredientForm

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    title = "Home"
    return render_template("home.html", title=title)

@main.route("/ingredients", methods=['GET', 'POST'])
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
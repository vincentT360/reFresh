from flask import render_template, request, Blueprint, redirect, url_for
from flaskdriver import db
from flaskdriver.models import GroceryItem
from flaskdriver.forms import AddGroceryItemForm

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    title = "Home"
    return render_template("home.html", title=title)

@main.route("/groceries", methods=['GET', 'POST'])
def pick_groceries():
    title = "Pick the groceries you want to get"
    form = AddGroceryItemForm()
    if form.validate_on_submit():
        new_item = GroceryItem(name=form.name.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.pick_groceries'))

    groceries = GroceryItem.query.order_by(GroceryItem.name).all()
    return render_template("pick_groceries.html", title=title, groceries=groceries, form=form)
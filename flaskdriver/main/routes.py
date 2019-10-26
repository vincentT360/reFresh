from flask import render_template, request, Blueprint, redirect, url_for
from flaskdriver import db
from flaskdriver.models import GroceryItem
from flaskdriver.forms import AddGroceryItemForm

main = Blueprint("main", __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    form = AddGroceryItemForm()
    if form.validate_on_submit():
        new_item = GroceryItem(name=form.name.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.home'))

    groceries = GroceryItem.query.order_by(GroceryItem.name).all()
    return render_template("home.html", title="Home", groceries=groceries, form=form)
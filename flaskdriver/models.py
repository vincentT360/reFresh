from flaskdriver import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class IngredientProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    image_url = db.Column(db.String(1000))
    price = db.Column(db.Float)
    quantity = db.Column(db.Float)
    quantity_type = db.Column(db.String(120))
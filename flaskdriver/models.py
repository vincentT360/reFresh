from flaskdriver import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)

class IngredientProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)
    image_url = db.Column(db.String(1000))
    price = db.Column(db.Float)
    quantity = db.Column(db.Float)
    quantity_type = db.Column(db.String(120))
    recipe_id = db.Column(db.Integer, db.ForeignKey('meal.id'))

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)
    ingredients = db.relationship('IngredientProduct', backref='meal', lazy='subquery')
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'))

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meals = db.relationship('Meal', backref='mealplan', lazy='subquery')


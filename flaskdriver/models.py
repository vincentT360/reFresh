from flaskdriver import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)

belong_to = db.Table('meals_belong_to',
                    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient_product.id')),
                    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'))
)

class IngredientProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)
    image_url = db.Column(db.String(1000))
    price = db.Column(db.Float)
    quantity = db.Column(db.Float)
    quantity_type = db.Column(db.String(120))
    belongs_to = db.relationship('Meal', secondary=belong_to, backref=db.backref('belongs_to', lazy='subquery'))

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'))

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meals = db.relationship('Meal', backref='mealplan', lazy='subquery')


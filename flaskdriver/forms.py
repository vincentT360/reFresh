from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddIngredientForm(FlaskForm):
    name = StringField('New Ingredient', validators=[DataRequired()])
    submit = SubmitField('Add item')
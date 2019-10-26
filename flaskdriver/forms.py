from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AddIngredientForm(FlaskForm):
    name = StringField('New Ingredient', validators=[DataRequired()])
    submit = SubmitField('Add ingredient')

class SearchRecipeForm(FlaskForm):
    name = StringField('Search for a recipe', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class ChooseRecipeForm(FlaskForm):
    select = SelectField('Choose recipe', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Choose recipe')
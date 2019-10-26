from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddGroceryItemForm(FlaskForm):
    name = StringField('New Grocery Item', validators=[DataRequired()])
    submit = SubmitField('Add item')
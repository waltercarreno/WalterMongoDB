from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=12)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password',
                                                                             message='Passwords must be the same.')])
    submit = SubmitField('Register')

class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    cooking_time = IntegerField('Cooking Time', validators=[DataRequired()])
    serving_size = IntegerField('Serving Size', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    recipe_image = StringField(
        'Copy Image Address Link', validators=[DataRequired()])
    submit = SubmitField('Create')

class EditRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    cooking_time = IntegerField('Cooking Time', validators=[DataRequired()])
    serving_size = IntegerField('Serving Size', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    recipe_image = StringField(
        'Copy Image Address Link', validators=[DataRequired()])
    submit = SubmitField('Update')


class DeleteForm(FlaskForm):
    username = StringField('username')
    submit = SubmitField('Delete')
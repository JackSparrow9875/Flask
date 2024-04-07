from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length


class UserForm(FlaskForm):
    name = StringField("Enter your Name", validators=[DataRequired()])
    email = StringField("Enter your Email", validators=[DataRequired()])
    address = StringField("Enter your Address", validators=[DataRequired()])
    password = PasswordField("Enter a Password", validators=[DataRequired()])
    password2 = PasswordField("Confirm Ppassword", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateUserForm(FlaskForm):
    updated_name = StringField("What is your new name?")
    updated_email = StringField("Enter your new email")
    updated_color = StringField("What is your new favorite color?")
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("Enter your registered email", validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class NewCategory(FlaskForm):
    cat_name = StringField("Enter the name of the category", validators=[DataRequired()])
    cat_description = StringField("Category description", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateCat(FlaskForm):
    update_cat_name = StringField("Enter the updated name of the category")
    update_cat_desp = StringField("Updated category description")
    submit = SubmitField("Submit")

class NewItem(FlaskForm):
    item_name = StringField("Enter the name of the item to be added", validators=[DataRequired()])
    item_price = StringField("Price of the Item", validators=[DataRequired()])
    date_added = DateField("From when is this Item going to be available", validators=[DataRequired()])
    availability = SelectField("Current Availability", choices=[('True', 'Yes'),('False', 'No')], validators=[DataRequired()])
    item_img = FileField('Upload Item Image', validators=[FileAllowed(['jpg','png']), DataRequired()])
    submit = SubmitField("Submit")

class UpdateItem(FlaskForm):
    update_item_name = StringField("Updated name of the item")
    update_item_price = StringField("Updated price of the item")
    update_availability = SelectField("Change availability", choices=[('True', 'Yes'), ('False','No')])
    update_item_img = FileField('Update the item image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Submit")
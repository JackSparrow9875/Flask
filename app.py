from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
from datetime import datetime, timezone


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NovaCart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    fav_color = db.Column(db.String(50))
    hashed_password = db.Column(db.String(128))

    def __repr__(self):
        return f"<User {self.name}>"

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100), unique=True)
    cat_description = db.Column(db.Text(1000))

    def __repr__(self):
        return f"<Category {self.cat_name}>"
    

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), unique=True)
    item_price = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    available = db.Column(db.Boolean, default=True)
    item_img = db.Column(db.String)

    def __repr__(self):
        return f"<Item {self.item_name}; Price: {self.item_price}; Available: {self.available}"


class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    fav_color = StringField("What is your favorite color?", validators=[DataRequired()])
    password = PasswordField("Enter your password", validators=[DataRequired()])
    password2 = PasswordField("Confirm password", validators=[DataRequired()])
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

#DEFINING ROUTES AND VIEWS
@app.route('/')
def index():
    items = Items.query.order_by(func.random()).limit(5).all()
    categories = Category.query.order_by(func.random()).limit(5).all()
    return render_template('home.html', items=items, categories=categories)

@app.route('/signin', methods=["GET", "POST"])
def signin():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #clearing the form
        (form.email.data, form.password.data) = ("","")
        
        #lookup user by email address
        pw_to_check = User.query.filter_by(email=email).first()
        #check hashed password
        passed = check_password_hash(pw_to_check.hashed_password, password)

    return render_template('userdashboard.html', email=email, password=password, pw_to_check=pw_to_check, passed=passed, form=form)


@app.route('/user_signup', methods=['GET','POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        fav_color = form.fav_color.data
        password = form.password.data
        password2 = form.password2.data
        if password == password2:
            hashed_password = generate_password_hash(password)
            try:
                new_user = User(name=name, email=email, fav_color=fav_color, hashed_password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully!', 'success')
                return redirect(url_for('user', name=name))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
        else:
            flash('Passwords do not match, please try again...', 'error')
    return render_template('usersignup.html', form=form)


@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def user_update(user_id):
    form = UpdateUserForm()
    user = User.query.get_or_404(user_id)
    if request.method == 'POST' and form.validate_on_submit():
        user.name = form.updated_name.data
        user.email = form.updated_email.data
        user.fav_color = form.updated_color.data
        try:
            db.session.commit()
            flash('User details updated successfully!')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
    return render_template('user_update.html', form=form, user=user)

@app.route('/user_list')
def userlist():
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/admin')
def admin():
    return render_template('admin.html')

#CATEGORIES
@app.route('/admin/new_category', methods=['GET', 'POST'])
def new_cat():
    cat_name = None
    cat_description = None
    form = NewCategory()
    if form.validate_on_submit():
        cat_name = form.cat_name.data
        cat_description = form.cat_description.data
        try:
            new_cat = Category(cat_name=cat_name, cat_description=cat_description)
            db.session.add(new_cat)
            db.session.commit()
            flash('Catergory added successfully')
        except Exception as e:
            flash(f'An error encountered: {str(e)}')
        #clearing the form
        form.cat_name.data = ""
        form.cat_description.data = ""
    return render_template('new_cat.html', form=form)

@app.route('/admin/category_list')
def category_list():
    categories = Category.query.all()
    return render_template('catlist.html', categories=categories)

@app.route('/admin/udpate_category/<int:cat_id>', methods=['GET','POST'])
def update_cat():
    #selecting all the categories
    categories = Category.query.all()

    if request.method=="POST":
        cat_id = request.form.get('cat_id')
        cat = Category.query.get_or_404(cat_id)
        form = UpdateCat()
        if request.method == 'POST' and form.validate_on_submit():
            cat.cat_name = form.update_cat_name.data
            cat.cat_description = form.update_cat_desp.data
            try:
                db.session.commit()
                flash(f'Category {cat.cat_name} has been updated successfully!')
            except Exception as e:
                flash(f'An error occured: {str(e)}')
        return render_template('update_cat.html', form=form, cat=cat, categories=categories)
    else:
        form = UpdateCat()
        return render_template('update_cat.html', form, categories=categories) 


#ITEMS
@app.route("/admin/add_items", methods=["GET", "POST"])
def add_item():
    item_name = None
    item_price = None
    date_added = None
    available = None
    item_img = None
    form = NewItem()
    if form.validate_on_submit():
        item_name = form.item_name.data
        item_price = form.item_price.data
        date_added = form.date_added.data
        available = form.availability.data == 'True'
        item_img = form.item_img.data

        filename = secure_filename(item_img.filename)
        item_img.save(os.path.join('./static/Images/', filename))
        try:
            new_item = Items(item_name=item_name, item_price=item_price, date_added=date_added, available=available, item_img=filename)
            db.session.add(new_item)
            db.session.commit()
            flash("New Item added successfully")
        except Exception as e:
            flash(f"An error encountered: {str(e)}")
        form.item_name.data = ""
        form.item_price.data = ""
        form.date_added.data = ""
        form.availability.data = ""
        form.item_img.data = ""
    return render_template("newitem.html", form=form)


@app.route("/item_list", methods=["GET", "POST"])
def item_list():
    items = Items.query.all()
    return render_template('itemslist.html', items=items)


@app.route('/admin/update_item/<int:item_id>', methods=['GET','POST'])
def update_item(item_id):
    form = UpdateItem()
    item = Items.query.get_or_404(item_id)
    if request.method == 'POST' and form.validate_on_submit():
        item.item_name = form.update_item_name.data
        item.item_price = form.update_item_price.data
        item.available = form.update_availability.data
        item.item_img = form.update_item_img.data
        try:
            db.session.commit()
            flash(f'{item.item_name}\'s details have been updated successfully!')
        except Exception as e:
            flash(f'An error occured: {str(e)}')
    return render_template('', form=form, item=item)


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(405)
def invalid_method(e):
    return render_template('405.html'), 405


if __name__ == "__main__":
    app.run(debug=True)

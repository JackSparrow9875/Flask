from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate


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

#DEFINING ROUTES AND VIEWS
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signin', methods=["GET", "POST"])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #clearing the form
        (form.email.data, form.password.data) = ("", "")
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
                flash('User added successfully!')
                return redirect(url_for('user', name=name))
            except Exception as e:
                flash(f'An error occurred: {str(e)}')
        else:
            flash('Passwords do not match, please try again...')
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

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key@123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NovaCart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    fav_color = db.Column(db.String(50))
    _password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    fav_color = StringField("What is your favorite color?", validators=[DataRequired()])
    password1 = PasswordField("Enter your password", validators=[DataRequired()])
    password2 = PasswordField("Re-enter your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateUserForm(FlaskForm):
    updated_name = StringField("What is your new name?")
    updated_email = StringField("Enter your new email")
    updated_color = StringField("What is your new favorite color?")
    submit = SubmitField("Submit")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return render_template('userdashboard.html', name=name)

@app.route('/user_signup', methods=['GET','POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        fav_color = form.fav_color.data
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 == password2:
            password = generate_password_hash(password1)
            try:
                new_user = User(name=name, email=email, fav_color=fav_color, _password=password)
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

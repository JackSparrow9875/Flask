from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import sqlite3


app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "secret_key@123"

con = sqlite3.connect('NovaCart.db')
cur = con.cursor()

class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    password1 = PasswordField("Enter your password", validators=[DataRequired()])
    password2 = PasswordField("Re-enter your password", validators=[DataRequired()])
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
    name = None
    email = None
    password = None
    if form.validate_on_submit():
        if form.password1.data == form.password2.data:
            name = form.name.data
            email = form.email.data
            password = form.password1.data
            cur.execute('''INSERT INTO Users(Name, Email, Password) VALUES (?,?,?)''', (name,email,password))
            con.commit()
            con.close()
            flash('User added successfully!')
            return redirect(url_for('user', name=name))
        else:
            flash("Passwords donot match, please try again")
    
    return render_template('usersignup.html', form=form)


#ERROR HANDLING
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
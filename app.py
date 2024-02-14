from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
from datetime import datetime

app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "secret_key@123"


class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/user_signup', methods=["GET", "POST"])
def usersignupform():
    name = None
    email = None
    form = UserForm()
    #validating the form
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        con = sqlite3.connect('NovaCart.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM Users WHERE Email=?", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            flash('User already exists')
        else:
            cur.execute("INSERT INTO Users(Name, Email) Values (?,?)", (name, email))
            con.commit()
            flash('Signup Successful!')
        con.close()
        form.name.data = ''
        form.email.data = ''
    
    return render_template('usersignup.html', name=name, email=email, form=form)

@app.route('/userslist')
def userslist():
    con = sqlite3.connect('NovaCart.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Users''')
    users = cur.fetchall()
    con.close()
    return render_template('userlist.html', users=users)

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
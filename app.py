from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
from datetime import datetime

app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "secret_key@123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///NovaCart.db'



class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    password1 = PasswordField("Enter your password", validators=[DataRequired()])
    password2 = PasswordField("Re-enter your password", validators=[DataRequired()])
    submit = SubmitField("Submit")


def get_cursor():
    con = sqlite3.connect('NovaCart.db')
    cur = con.cursor()
    return con, cur


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
            try:
                con, cur = get_cursor()
                cur.execute('''INSERT INTO Users(Name, Email, Password) VALUES (?,?,?)''', (name,email,password))
                con.commit()
                flash('User added successfully!')
                return redirect(url_for('user', name=name))
            except sqlite3.Error as e:
                flash(f'An error occured: {str(e)}')
            finally:
                if con:
                    con.close()
        else:
            flash("Passwords donot match, please try again")
    
    return render_template('usersignup.html', form=form)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    con, cur = get_cursor()
    cur.execute("SELECT * FROM Users WHERE id=?", (id,))
    user = cur.fetchone()
    if user is None:
        flash('Error! User does not exist')
    
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        try:
            cur.execute('''UPDATE Users SET Name=?, Email=? WHERE id=?''', (name,email,id))
            con.commit()
            flash('User information updated successfully!')
            return render_template('update_user.html', form=form)
        except sqlite3.Error as e:
            flash(f'An error occurred: {str(e)}')
        finally:
            if con:
                con.close()
    elif request.method == 'GET':
        form.name.data = user[1]
        form.email.data = user[2]
        form.password1.data = user[3]
    return render_template('update_user.html', form=form, id=id)

@app.route('/user_list')
def userlist():
    try:
        con, cur = get_cursor()
        cur.execute('''SELECT * FROM Users''')
        users = cur.fetchall()
        return render_template('userlist.html', users=users)
    except Exception as e:
        flash(f'An error occured: {str(e)}')
    finally:
        if con:
            con.close()

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
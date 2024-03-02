from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "secret_key@123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///NovaCart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    fav_color = StringField("What is you favrouite color?", validators=[DataRequired()])
    password1 = PasswordField("Enter your password", validators=[DataRequired()])
    password2 = PasswordField("Renter your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateUserForm(FlaskForm):
    updated_name = StringField("What is new your name?")
    updated_email = StringField("Enter your new email")
    updated_color = StringField("What is you new favrouite color?")
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
    fav_color = None
    password1 = None
    password2 = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        fav_color = form.fav_color.data
        password1 = form.password1.data
        password2 = form.password2.data
        if password1 == password2:
            password = password1
            try:
                con, cur = get_cursor()
                cur.execute('''INSERT INTO Users(Name, Email, Fav_Color, Password) VALUES (?,?,?,?)''', (name,email,fav_color,password))
                con.commit()
                flash('User added successfully!')
                return redirect(url_for('user', name=name))
            except sqlite3.Error as e:
                flash(f'An error occured: {str(e)}')
            finally:
                if con:
                    con.close()
        else:
            flash('Oops! Passwords entered donot match, please try again...')
    return render_template('usersignup.html', form=form)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def user_update(user_id):
    form = UpdateUserForm()
    con, cur = get_cursor()
    cur.execute('''SELECT * FROM Users WHERE ID = ?''', (user_id,))
    user = cur.fetchone()
    name_placeholder = user[1]
    email_placeholder = user[2]
    color_placeholder = user[3]
    con.close()
    updated_name = None
    updated_email = None
    updated_color = None
    if request.method == 'POST' and form.validate_on_submit():
        updated_name = form.updated_name.data
        updated_email = form.updated_email.data
        updated_color = form.updated_color.data
        try:
            con, cur = get_cursor()
            cur.execute('''UPDATE Users SET Name=?, Email=?, Fav_Color=? WHERE id=?''', (updated_name, updated_email, updated_color, user_id))
            con.commit()
            flash('User details updated successfully!')
        except sqlite3.Error as e:
            flash(f'An error occurred: {str(e)}')
        finally:
            if con:
                con.close()
    return render_template('user_update.html', form=form, updated_name=updated_name, user_id=user_id,
                           prev_name = name_placeholder, prev_email = email_placeholder, prev_color = color_placeholder)

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
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "secret_key@123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/NovaCart.db'
#adding database
db = SQLAlchemy(app)

#defining the model
class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' %self.name
    
class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


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

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
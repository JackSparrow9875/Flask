from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/about/<username>')
def about_page(username):
    return f'<h1>About {username}</h1>'

# if __name__ == "__main__":
#     app.run(debug=True)
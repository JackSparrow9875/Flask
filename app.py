from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/categories')
def categories():
    categories = [
        {"id": 1, "name": "Electronics", 'description': "Latest gadgets and tech accessories"},
        {"id": 2, "name": "Clothing", 'description': "Fashionable apparel for all occasions"},
        {"id": 3, "name": "Home and Furniture", 'description': "Stylish and functional home decor"},
        {"id": 4, "name": "Sports and Outdoors", 'description': "Equipment for sports and outdoor activities"},
        {"id": 5, "name": "Books and Literature", 'description': "A wide range of books for all interests"},
        {"id": 6, "name": "Beauty and Personal Care", 'description': "Skincare, cosmetics, and personal care products"},
        {"id": 7, "name": "Toys and Games", 'description': "Fun and educational toys and games"},
        {"id": 8, "name": "Automotive", 'description': "Car accessories and maintenance products"},
        {"id": 9, "name": "Health and Wellness", 'description': "Health supplements and wellness products"},
        {"id": 10, "name": "Appliances", 'description': "Home appliances for convenience"},
        {"id": 11, "name": "Jewelry and Accessories", 'description': "Elegant jewelry and fashion accessories"},
        {"id": 12, "name": "Food and Beverages", 'description': "Delicious food and beverage items"},
        {"id": 13, "name": "Office Supplies", 'description': "Stationery and office essentials"},
        {"id": 14, "name": "Pet Supplies", 'description': "Products for your furry friends"},
        {"id": 15, "name": "Garden and Outdoor Living", 'description': "Gardening tools and outdoor decor"}
        ]
    return render_template('categories.html', categories = categories)

# @app.route

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/categories')
def categories():
    categories = [
    {"CategoryID": 1, "CategoryName": "Electronics", "Description": "Latest gadgets and tech accessories"},
    {"CategoryID": 2, "CategoryName": "Clothing", "Description": "Fashionable apparel for all occasions"},
    {"CategoryID": 3, "CategoryName": "Home and Furniture", "Description": "Stylish and functional home decor"},
    {"CategoryID": 4, "CategoryName": "Sports and Outdoors", "Description": "Equipment for sports and outdoor activities"},
    {"CategoryID": 5, "CategoryName": "Books and Literature", "Description": "A wide range of books for all interests"},
    {"CategoryID": 6, "CategoryName": "Beauty and Personal Care", "Description": "Skincare, cosmetics, and personal care products"},
    {"CategoryID": 7, "CategoryName": "Toys and Games", "Description": "Fun and educational toys and games"},
    {"CategoryID": 8, "CategoryName": "Automotive", "Description": "Car accessories and maintenance products"},
    {"CategoryID": 9, "CategoryName": "Health and Wellness", "Description": "Health supplements and wellness products"},
    {"CategoryID": 10, "CategoryName": "Appliances", "Description": "Home appliances for convenience"},
    {"CategoryID": 11, "CategoryName": "Jewelry and Accessories", "Description": "Elegant jewelry and fashion accessories"},
    {"CategoryID": 12, "CategoryName": "Food and Beverages", "Description": "Delicious food and beverage items"},
    {"CategoryID": 13, "CategoryName": "Office Supplies", "Description": "Stationery and office essentials"},
    {"CategoryID": 14, "CategoryName": "Pet Supplies", "Description": "Products for your furry friends"},
    {"CategoryID": 15, "CategoryName": "Garden and Outdoor Living", "Description": "Gardening tools and outdoor decor"}
    ]
    return render_template('categories.html', categories = categories)

# @app.route

if __name__ == "__main__":
    app.run(debug=True)
from app import app, db

#ONLY NEEDS TO BE RUN ONCE FOR DATABASE CREATION
with app.app_context():
    db.create_all()
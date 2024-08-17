from app import db
from models import User, Report

def create_database():
    db.create_all()
    print("Database tables created.")

if _name_ == '_main_':
    create_database()
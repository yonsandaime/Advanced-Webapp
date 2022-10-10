#Bevat de database modellen.

from app import db
from flask_login import UserMixin

#De gebruikte 'User' class wordt als subclass voortgebouwd bovenop: 
# - flask-login UserMixin: bevat de benodigde flask-login zaken
# - db.model (komend van SQLAlchemy): ORM database mapping
class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False)
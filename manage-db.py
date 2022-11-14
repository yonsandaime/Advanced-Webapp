#Uitvoeren om de sqlite database en bijhorende tabellen te initialiseren aan de hand van de gedefinieerde modellen.
#via: python manage-db.py

def init_db():
	"""Initialize database(s)."""
	from app import create_app,db
	from models import User,Entries
	
	app = create_app()
	app.app_context().push()
	db.create_all()

	
init_db()
from app import create_app, login_manager, db, bcrypt
from models import User

import flask, flask_login

# opstarten app (initialiseert alle flask modules)
app = create_app()



#flask-login user_loader functie controleert bij elk pagina verzoek de geldigheid van de sessie
@login_manager.user_loader
def load_user(user_id):
    print("flask-login: user_loader functie opgeroepen om geldigheid user sessie %s te controleren." % user_id)
    return User.query.get(int(user_id))


#flask-login custom unauthorized handler. Wordt uitgevoerd indien niet ingelogd of ongeldig...
@login_manager.unauthorized_handler
def unauthorized():
    return flask.render_template('unauthorized.html')    



#index template geeft andere inhoud afhankelijk of gebruiker is ingelogd of niet. Bekijk template...
@app.route('/')
def index():
    return flask.render_template('index.html')


#home template geeft bepaalde inhoud van de user sessie.
#enkel toegankelijk indien gebruiker ingelogd.
@app.route('/home')
@flask_login.login_required
def home():
    #print(vars(flask_login.current_user))
    return flask.render_template('home.html')

#logout route. Roept de flask-login logout_user() functie op om de gebruikersessie te stoppen.
@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out <a href="' + flask.url_for('index') + '">Index</a>'

#Login route. GET methode voor weergeven login formulier. POST methode om login formulier te verwerken.
#Controleert of username & password overeen komen met database
#Roept de flask-login login_user(user) functie op indien correct, waarbij user de overeenkomende inhoud bevat volgens User model.
#TODO: Gebruik bcrypt voor paswoord salting + hashing
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':

        try:
            user = User.query.filter_by(username=flask.request.form['username']).first()
            if user and user.pwd and user.pwd == flask.request.form['password']:
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('home'))
            else:
                return "Invalid username or password..."
        except Exception as e:
            print(e)
            return e
    else:
        return flask.render_template('login.html')

#Register route. GET methode voor weergeven register formulier. POST methode om register formulier te verwerken.
#Maakt nieuwe user aan.
#Nieuwe user wordt daarbij ook gepusht naar database.
#TODO: zorg dat password met bcrypt wordt gesalt en gehashed.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        try:
            newUser = User(
                username = flask.request.form['username'], 
                pwd = flask.request.form['password']
            )
            db.session.add(newUser)
            db.session.commit()
            return flask.redirect(flask.url_for('login'))
        except Exception as e:
            print(e)
            return e
    else:
        return flask.render_template('register.html')


# Webserver opstarten
if __name__ == "__main__":
    app.run(host='localhost', port=8080)
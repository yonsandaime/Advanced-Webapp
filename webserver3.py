import pwd
from app import create_app, login_manager, db, bcrypt
from models import User,Entries
import coapclient
import asyncio
from flask_socketio import SocketIO
from datetime import datetime
import sqlite3
con = sqlite3.connect("instance/database.db")

import flask, flask_login
import threading
access = True

lampdict = {
  "lamp1a": 0,
  "lamp1b": 0,
  "lamp1c": 0,
  "lamp2a": 0,
  "lamp2b": 0,
  "lamp2c": 0,
  "lamp3a": 0,
  "lamp3b": 0,
  "lamp3c": 0,
  "lamp4a": 0,
  "lamp4b": 0,
  "lamp4c": 0,
  "lamp5a": 0,
  "lamp5b": 0,
  "lamp5c": 0
}


# opstarten app (initialiseert alle flask modules)
app = create_app()
socketio = SocketIO(app, async_mode='eventlet')
import eventlet
eventlet.monkey_patch()

@socketio.on('connect')
def socketioconnected():
    print("Socketio session connected.", flask.request.sid)

@socketio.on('disconnect')
def socketiodisconnected():
    print("Socketio disconnected.")

@socketio.on('changeLampValue')
def changevalue(content):
    print("Value received: %s from %s" % (content, str(flask.request.sid)))
    socketio.emit('ReceiveLampValue', content)

def getValues():
    global lampdict
    threading.Timer(15.0, getValues).start()
    kolommen = ['a','b','c']
    for rij in range(1,6):
        for kolom in kolommen:
            val = asyncio.run(coapclient.coapgetlampstatus('coap://lamp'+str(rij)+kolom+'.irst.be/lamp/dimming'))
            lampdict["lamp"+str(rij)+kolom] = str(int(val))
    #print(lampdict)
    socketio.emit('UpdateValues', lampdict)
    
getValues()


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
    #return flask.render_template('home.html')
    
    return flask.render_template('gwa1.html')

@app.route('/history')
@flask_login.login_required
def history():
    cur = con.cursor()
    cur.execute("SELECT * FROM entries ORDER BY entryid DESC")
    data = cur.fetchall()
    return flask.render_template('history.html',data=data)
    
    

#logout route. Roept de flask-login logout_user() functie op om de gebruikersessie te stoppen.
@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.render_template('logout.html')

@app.route('/api/<lamp>',methods = ['GET', 'POST', 'PUT']) #Create link of the website
@flask_login.login_required
def test(lamp):
    if flask.request.method == 'GET':
        global lampdict
        if (lamp == "lampAllemaal"):
            return "0"
        else:
            return lampdict[lamp]
    
    elif flask.request.method == 'POST' or flask.request.method == 'PUT':
        if 'dimming' in flask.request.form:
            value = flask.request.form['dimming']
            print(value)
        else:
            return('error: :Missing dimming payload. )',400)

        now = datetime.now()
        newEntry = Entries(username = flask_login.current_user.username,entrylamp = lamp,entryvalue = value, time = now.strftime("%m/%d/%Y, %H:%M:%S"))
        db.session.add(newEntry)
        db.session.commit()
        asyncio.run(coapclient.coapsetlampstatus('coap://'+lamp+'.irst.be/lamp/dimming',str.encode(str(value))))
        return {'result':'OK'}

    else:
        return ({'error':'not supported'},405)

@app.route('/api/lampAllemaal',methods = ['POST', 'PUT']) #Create link of the website
@flask_login.login_required
def test2():
    if flask.request.method == 'POST' or flask.request.method == 'PUT':
        if 'dimming' in flask.request.form:
            value = flask.request.form['dimming']
            print(value)
        else:
            return('error: :Missing dimming payload. )',400)

        now = datetime.now()
        newEntry = Entries(username = flask_login.current_user.username,entrylamp = "All lamps",entryvalue = value, time = now.strftime("%m/%d/%Y, %H:%M:%S"))
        db.session.add(newEntry)
        db.session.commit()

        kolommen = ['a','b','c']
        for rij in range(1,6):
            for kolom in kolommen:
                asyncio.run(coapclient.coapsetlampstatus('coap://lamp'+str(rij)+kolom+'.irst.be/lamp/dimming',str.encode(str(value))))
        return {'result':'OK'}

    else:
        return ({'error':'not supported'},405)


#Login route. GET methode voor weergeven login formulier. POST methode om login formulier te verwerken.
#Controleert of username & password overeen komen met database
#Roept de flask-login login_user(user) functie op indien correct, waarbij user de overeenkomende inhoud bevat volgens User model.
#TODO: Gebruik bcrypt voor paswoord salting + hashing
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':

        try:
            user = User.query.filter_by(username=flask.request.form['username']).first()
            if user and user.pwd and bcrypt.check_password_hash(user.pwd,flask.request.form['password']):
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('home'))
            else:
                return flask.render_template("login.html", msg = "Invalid Username or Password... Please try again")
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
                pwd = bcrypt.generate_password_hash(flask.request.form['password'],12).decode('utf-8')
            )
            cur = con.cursor()
            cur.execute("SELECT username FROM user")
            users = cur.fetchall()
            users = [elem[0] for elem in users]
            print(users[3])
            print(newUser.username)
            if newUser.username in users:
                return flask.render_template('register.html',msg = "This username already exists. Please chose another one")
            else:
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
    #app.run(host='localhost', port=8081,debug=True)
    socketio.run(app, host='localhost', port=8081, debug=True, use_reloader=False)

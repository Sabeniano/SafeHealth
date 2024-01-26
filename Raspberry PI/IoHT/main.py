import folium
import threading
import encryption
from mqtt import mqtt_listener
from models import Bruger, Koordinater, Promille, Faldet
from flask import Flask, g, render_template, request, url_for, redirect, session

#Starter mqtt som lytter på gps_data_topic
thread = threading.Thread(target=mqtt_listener())
thread.start()

app = Flask(__name__, static_folder='static')
app.secret_key = 'SDSDSHFT23213213FDSFSDF'

#Funktion der starter hver gang der er en HTTP request
@app.before_request
def before_request():
    if 'produkt_id' in session:
        produkt_id = session['produkt_id']
        user = Bruger.find_by_produkt_id(produkt_id)
        if user:
            g.user = user

@app.route("/")
def index():
     return render_template('index.html')

#TODO opret
@app.route("/registrer", methods=['GET', 'POST'])
def registrer():
    if request.method == 'POST':
        registrer = request.form.get('produkt_id')
    else:
        return render_template('index.html')

@app.route("/index", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        produkt_id = request.form.get('produkt_id')

        produkt = Bruger.find_by_produkt_id(produkt_id)
        if produkt:
            session['produkt_id'] = produkt.produkt_id
            return redirect(url_for('profil'))
        else:
            error = 'Produkt ID not found in database'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')
    
@app.route("/profil")
def profil():
    if g.user:
        produkt_id = g.user.produkt_id
        koordinater = Koordinater.find_by_produkt_id(produkt_id)
        promille = Promille.find_by_produkt_id(produkt_id)
        faldet = Faldet.find_by_produkt_id(produkt_id)

        latitude, longitude = 55.69178, 12.55388  # Default location
        if koordinater:
            latitude = encryption.decrypt_data(koordinater.latitude)
            longitude = encryption.decrypt_data(koordinater.longitude)
            print(latitude, longitude)

        # Create the map centered on the user's location
        m = folium.Map(location=[latitude, longitude], zoom_start=13)
        folium.Marker(location=[latitude, longitude], popup='Lokation').add_to(m)

        # Render the profil.html with user information and the map
        return render_template('profil.html', user=g.user, map=m._repr_html_(), promille=promille, faldet=faldet)
    else:
        return redirect(url_for('index'))

@app.route("/dashboard")
def dashboard():
    ##TODO Liste af alle brugere, hvor man bliver notificeret
    return render_template('dashboard.html')

@app.route("/logout")
def logout():
    session.pop('produkt_id', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')

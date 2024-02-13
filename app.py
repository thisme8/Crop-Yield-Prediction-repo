from flask import Flask, render_template, render_template_string, redirect, request, jsonify
from flask import session
import folium
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sqlalchemy_utils import database_exists
from sqlalchemy import func, exc
import requests
import pandas as pd
district_coordinates='district_abcd.csv'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/index", methods=['GET','POST']) 
def index_page():
    return render_template("index.html")



def get_soil_properties(latitude, longitude):
    url = f"http://soil.narc.gov.np/soil/api/soildata?lat={latitude}&lon={longitude}"

    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soil_data = response.json()
            return soil_data
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


        latitude = 28.746
        longitude = 80.695
        result = get_soil_properties(latitude, longitude)
        return render_template('analysis.html',result)
    
    
@app.route("/analysis", methods=['GET','POST'])
def analysis():
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    soil_data = get_soil_properties(latitude, longitude)
    return render_template('analysis.html', soil_data=soil_data)


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form.get('name',False)
        email = request.form.get('email',False)
        password = request.form['password']

        new_user = Users(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/board')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')




@app.route('/board')
def board():
    if session['email']:
        user = Users.query.filter_by(email=session['email']).first()
        return render_template('board.html',user=user)
    
    return redirect('/login')



@app.route("/logout")
def logout_page():
    if 'email' in session:
      session.pop('email',None)
    return redirect('/index')



@app.route("/prediction")
def prediction():
    #longitude = request.args.get('longitude', type=float)
    #latitude = request.args.get('latitude', type=float)
    return render_template('prediction.html')
    



@app.route("/aboutus")
def aboutus_page():
        return render_template('aboutus.html')



@app.route('/forms',methods=['GET','POST'])
def forms():
  longitude = request.args.get('longitude', type=float)
  latitude = request.args.get('latitude', type=float)

  return render_template("forms.html", longitude=longitude, latitude=latitude)

@app.route('/aboutus',methods=['GET','POST'])
def aboutus():
  return render_template("aboutus.html")



''' add layers control over the map
folium.TileLayer('openstreetmap', attr='openstreetmap').add_to(mapObj)
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
	attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
).add_to(mapObj)

folium.LayerControl().add_to(mapObj)

mapObj.save('fol.html')

#mapObj'''


'''@app.route("/") #this is a decorator
#def home():
    #return "</h1>Hello, Bitches!!Suck on it </br>real hard </h1>" '''


'''mapObj = folium.Map(location=[27.9928478,84.5296624], zoom_start=7.5, tiles=None)

# add layers control over the map
folium.TileLayer('openstreetmap', attr='openstreetmap').add_to(mapObj)
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', 
	attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community').add_to(mapObj)

folium.LayerControl().add_to(mapObj)

mapObj.save('fol.html')'''


#1 =>to run it in browser
#export set FLASK_APP=index.py(ie.appname)
#flask run 

#2 =>to sync the browser with changes 
#export set FLASK_DEBUG=1
#flask run

#3 =>render_template knows how to handle your request and direct them into html files
 
#4 => this allows you to refer our routes into different html files


if __name__ == '__main__':
    app.run(debug=True)

##@app.route('/login',methods=['GET','POST'])
##def login():
  ##  if request.method == 'POST':
    ##    email = request.form['email']
      ##  password = request.form['password']
##
  ##      user = User.query.filter_by(email=email).first()
    ##    
      ##  if user and user.check_password(password):
        ##    session['email'] = user.email
          ##  return redirect('/dashboard')
       # else:
        #    return render_template('login.html',error='Invalid user')
#
 #   return render_template('login.html')
 
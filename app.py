from flask import Flask, render_template, url_for, flash, redirect,request, Markup
from forms import RegistrationForm, LocationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from place_details import get_nearby_restaurants
from geo_code import get_coordinates

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = '159afc1053d04e47b66ac44bd36875fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
default_city = "Chicago"

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  location = db.Column(db.String(200), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# Route for handling the search page logic (extends index)
@app.route("/search", methods = ['GET','POST'])
def search():
    form = LocationForm()
    if form.validate_on_submit():
        city = form.City.data
        restaurants = get_nearby_restaurants(get_coordinates(city))
        # TODO: insert user location into database ONLY IF USER IS LOGGED-IN
        return render_template('search.html', form=form, restaurants=restaurants)

    default_restaurants = get_nearby_restaurants(get_coordinates(default_city))
    return render_template("search.html", form=form, restaurants=default_restaurants)


# Route for handling the index page logic
@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("index.html")


# Route for handling the register page logic
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
      if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        email = request.form.get('email')
        user = User.query.filter_by(username=username).first()
        another_user = User.query.filter_by(email=email).first()

        print(user, another_user)
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            message = Markup("<h4>Username already taken. Click <a href='/login'>here</a> to login <br> Click <a href='/'>here</a> to sign-up with a different username</h4>")
            flash(message)
            return render_template('blank.html')
        elif another_user: # if a user is found, we want to redirect back to signup page so user can try again
            message = Markup("<h4>Email already used. Click <a href='/login'>here</a> to login <br> Click <a href='/'>here</a> to sign-up with a different email</h4>")
            flash(message)
            return render_template('blank.html')

        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        #flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Sign-Up', form=form)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('username')
        user = User.query.filter_by(username=user_name).first()
        #if not user or not user.password:
        if request.form['username'] != user.username or request.form['password'] != user.password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
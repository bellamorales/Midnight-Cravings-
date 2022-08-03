from flask import (
    Flask, render_template, url_for,
    flash, redirect,request, Markup, g, session)
from forms import RegistrationForm, LocationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from place_details import get_nearby_restaurants
from geo_code import get_coordinates
import functools

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = '159afc1053d04e47b66ac44bd36875fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
default_city = "Chicago"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(20), unique=False, nullable=False)
  last_name = db.Column(db.String(20), unique=False, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.first_name}','{self.last_name}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def login_required(func):
    @functools.wraps(func)
    def secure_function(**kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return func(**kwargs)

    return secure_function


# Route for handling the main search page logic (extends index)
@app.route("/search", methods = ['GET','POST'])
@login_required
def search():
    form = LocationForm()
    if form.validate_on_submit():
        city = form.City.data
        restaurants = get_nearby_restaurants(get_coordinates(city))
        # TODO: insert user location into database ONLY IF USER IS LOGGED-IN
        return render_template('search.html', form=form, email=session['email'], restaurants=restaurants)

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
    # if form.validate_on_submit(): # checks if entries are valid
    if request.method == 'POST':
        # flash(f'Account created for {form.first_name.data}!', 'success')
        # print("it is working")
        # return redirect(url_for('index')) # if so - send to home page
    # form = RegistrationForm()
    # if form.validate_on_submit(): # checks if entries are valid
    #   if request.method == 'POST' and form.validate():
    #       # checks if entries are valid
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            return flash("User already exist")
        password = request.form.get('password')
        user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=generate_password_hash(password, method='sha256'))
        print(user)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.first_name.data}!', 'success')

        # send to login page after registering account
        return redirect(url_for('login'))
        # firstname = request.form.get('first_name')
        # lastname = request.form.get('last_name')
        # email = request.form.get('email')
        # password = request.form.get('password')
        # user = User(first_name=firstname.data,
        #             last_name=lastname.data,
        #             email=email.data,
        #             location=city.data,
        #             password=generate_password_hash(password, method='sha256'))
        #another_user = User.query.filter_by(email=email).first()

        #print(user, another_user)
        #if user: # if a user is found, we want to redirect back to signup page so user can try again
            #message = Markup("<h4>Username already taken. Click <a href='/login'>here</a> to login <br> Click <a href='/'>here</a> to sign-up with a different username</h4>")
            #flash(message)
            #return render_template('blank.html')
        #elif another_user: # if a user is found, we want to redirect back to signup page so user can try again
            #message = Markup("<h4>Email already used. Click <a href='/login'>here</a> to login <br> Click <a href='/'>here</a> to sign-up with a different email</h4>")
            #flash(message)
            #return render_template('blank.html')

        # new_user = User(firstname=form.first_name.data,lastname=form.last_name.data, email=form.email.data, password=form.password.data)
        # db.session.add(new_user)
        # db.session.commit()
        # #flash(f'Account created for {form.username.data}!', 'success')
        # return redirect(url_for('index')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                session.clear()
                session['email'] = email
                return redirect(url_for('search'))
            else:
                error = 'Invalid Password. Please try again.'
        else:
            error = "Invalid email. Please try again."
        return render_template('login.html', error=error, form=form)

    return render_template('login.html', error=error, form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
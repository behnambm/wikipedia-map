from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasksitedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.secret_key = 'B\x00k\x94?-\x06\\\x95>TZ\x83\xd0T\xcd\xb0\x0e\x82\xd5\x93\xd9R\xd4q\xecT\x8a+\x97.B'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else:   # this means user entered the correct data
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)                
            db.session.commit()
            session['email'] = newuser.email
            session['firstname'] = newuser.firstname
            session['lastname'] = newuser.lastname
            return redirect(url_for('home'))

    else:
        return render_template('signup.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    form = AddressForm()
    places = []
    my_coordinates = (37.5493473, 45.0682863)

    if request.method == 'POST':
        if not form.validate():
            return render_template('home.html', form=form, coordinates=my_coordinates, places=places, msg=' ')
        else:
            address = form.address.data 
            radius = form.radius.data
            p = Place()
            my_coordinates = p.address_to_latlong(address)
            places = p.query(address, radius)
            if not places:
                return render_template('home.html', form=form, coordinates=my_coordinates, msg='Place not found.')
            return render_template('home.html', form=form, coordinates=my_coordinates, places=places)
    else: 
        return render_template('home.html', form=form, coordinates=my_coordinates, places=places, msg=' ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = email
                session['firstname'] = user.firstname
                session['lastname'] = user.lastname
                return redirect(url_for('home'))
            else:
                return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/signout')
def signout():
    session.pop('email', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    # app.run(port=80, host='0.0.0.0')
    app.run()
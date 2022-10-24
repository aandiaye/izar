from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = "ziza1529"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///izar.db"
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    password = db.Column(db.String)

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_verify = db.session.execute(db.select(User).where(User.email == request.form["email"])).first()
        if user_verify is None:
            password = generate_password_hash(request.form["password"], method='sha256')
            user = User(
                firstname=request.form["firstname"],
                lastname = request.form["lastname"],
                email = request.form["email"],
                phone = request.form["phone"],
                password = password,)
            db.session.add(user)
            db.session.commit()
            #TODO voir pourquoi les messages flash ne s'affiche pas
            flash("You are registered and can now login", "success")
            return redirect(url_for('login'))
        else:
            flash("user already existed, please login or contact admin", "danger")
            return redirect(url_for('login'))
    else:
        if 'user_id' in session:
            return redirect(url_for('home'))
        else:
            return render_template('pages/register.html')


@app.route('/home')
def home():
    if "user_id" in session:
        user_id = session['user_id']
        lastname = session['lastname']
        email = session['login']
        return render_template('pages/index.html', data=[user_id,lastname,email])
    else:
        return redirect(url_for('login'))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email = request.form["email"]).first()
        if user is not None:
            if user.check_password(secret=request.form["password"]):
                session['user_id'] = user.id
                session['login'] = user.email
                session['lastname'] = user.lastname
                return redirect(url_for('home'))
            else:
                message="identifiant ou mot de passe incorrect"
                return render_template('pages/login.html', message=message)
        else :
            message = "identifiant ou mot de passe incorrect"
            return render_template('pages/login.html', message=message)
    else :
        if "user_id" in session:
            return redirect(url_for('home'))
        else:
            message = "Authentification"
            return render_template('pages/login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('lastname', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5005, debug=True)



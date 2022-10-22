from flask import Flask, render_template, request, redirect, url_for, flash
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


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
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
            #TODO utiliser render template et rediriger vers login
            flash("You are registered and can now login", "success")
            return redirect(url_for('login'))
        else :
            # TODO utiliser render template et rediriger vers register
            flash("user already existed, please login or contact admin", "danger")
            return redirect(url_for('login'))


@app.route('/')
def login():
    message = 'Welcome Back!'
    return render_template('pages/login.html', message = message)


@app.route('/register')
def register():
    return render_template('pages/register.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5005, debug=True)



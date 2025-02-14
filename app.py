from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_manager, login_user, UserMixin, LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisIsSecretKey'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    firstName = db.Column(db.String(120), nullable = False)
    lastName = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(120), nullable = False)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/register", methods = ["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("formUsername")
        email = request.form.get("formEmail")
        firstName = request.form.get("formFirstName")
        lastName = request.form.get("formLastName")
        password = request.form.get("formPassword")

        user = User(username = username, email = email, firstName = firstName, lastName = lastName, password = password)
        db.session.add(user)
        db.session.commit()
        
        flash("User has been Registered Successfully.", "success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("formUsername")
        password = request.form.get("formPassword")
        
        user = User.query.filter_by(username = username).first()
        if user and password == user.password:
            login_user(user)
            return redirect("/")
        else:
            flash("Invalid Credentials", "warning")
            return redirect("/login")

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
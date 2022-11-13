from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
#from sqlalchemy.sql import exists

from passlib.hash import sha256_crypt

engine = create_engine("mysql+pymysql://root:@localhost/register")

db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

#register-form

@app.route("/register",methods=["GET","POST"])
def register():
   if request.method == "POST":
       name = request.form.get("name")
       username = request.form.get("username")
       password = request.form.get("password")
       confirm = request.form.get("confirm")
       secure_password = sha256_crypt.encrypt(str(password))

       arr = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
       if arr is not None:
        for i in arr:
         if i == username:
            flash("Username already exits, use a different username","danger")
            return render_template("register.html")

       if password == confirm:
           db.execute("INSERT INTO users(name, username, password) VALUES(:name,:username,:password)",{"name":name,"username":username,"password":secure_password})
           db.commit()
           flash("Registration succesfully completed, you can login now","success")
           return redirect(url_for('login'))
       else:
            flash("password does not match","danger")
            return render_template("register.html")
   return render_template("register.html")

#login

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passwordata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()

        if usernamedata is None:
            flash("Username not found, enter a valid username","danger")
            return render_template("login.html")
        else:
            for passwor_data in passwordata:
                if sha256_crypt.verify(password,passwor_data):
                    flash("You've been logged in","success")
                    return redirect(url_for('photo'))
                else:
                    flash("Incorrect password","danger")
                    return render_template("login.html")

    return render_template("login.html") 


#photo
@app.route("/photo")
def photo():
    return render_template("photo.html")

#logout
@app.route("/logout")
def logout():
    flash("You've been logged out","success")
    return redirect(url_for('login'))
    
if __name__ == "__main__":
    app.secret_key="1234567dailywebcoding"
    app.run(debug=True)

    
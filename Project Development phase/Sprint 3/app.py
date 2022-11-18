from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
#from sqlalchemy.sql import exists

from passlib.hash import sha256_crypt

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

engine = create_engine("mysql+pymysql://root:@127.0.0.1/register")

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
       email = request.form.get("email")
       secure_password = sha256_crypt.encrypt(str(password))

       arr = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
       if arr is not None:
        for i in arr:
         if i == username:
            flash("Username already exits, use a different username","danger")
            return render_template("register.html")

       if password == confirm:
           db.execute("INSERT INTO users(name, username, password, email) VALUES(:name,:username,:password,:email)",{"name":name,"username":username,"password":secure_password,"email":email})
           db.commit()


           message = Mail(
                  from_email='nashbarath@gmail.com',
                  to_emails= email ,
                  subject='Sending with Twilio SendGrid is Fun',
                  html_content='<strong>and easy to do anywhere, even with Python</strong>')
           try:
                  sg = SendGridAPIClient('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')
                  response = sg.send(message)
                  print(response.status_code)
                  print(response.body)
                  print(response.headers)
           except Exception as e:
                  print(e.message)
 

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
                    #flash("You've been logged in","success")
                    return redirect(url_for('index'))
                else:
                    flash("Incorrect password","danger")
                    return render_template("login.html")

    return render_template("login.html") 


#photo
@app.route("/index")
def index():
    return render_template("index.html")

#logout
@app.route("/logout")
def logout():
    #flash("You've been logged out","success")
    return redirect(url_for('login'))

#about 
@app.route("/about")
def about():
    return render_template("about.html")

#contact
@app.route("/contact")
def contact():
    return render_template("contact.html")

    
if __name__ == "__main__":
    app.secret_key="1234567dailywebcoding"
    app.run(debug=True)

    


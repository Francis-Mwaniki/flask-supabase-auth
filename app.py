
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from supabase import create_client, Client
from gotrue.errors import AuthApiError

# create a new Flask app
app = Flask(__name__)

url="your-supabase-url"
key="your-anon-key"
supabase: Client = create_client(url, key)

# home page
@app.route("/")
def home():
    return render_template("home.html")


""" 
res = supabase.auth.sign_up({
  "email": 'example@email.com',
  "password": 'example-password',
}) """

# create a new user /register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        password = data["password"]
        # use AuthApiError to handle errors
        print(f'Email: {email}, Password: {password}')
        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            print(res)
            return redirect(url_for("success"))
        except AuthApiError as e:
            print(e)
            return render_template("register.html", message="Invalid credentials")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data["email"]
        password = data["password"]
        # use AuthApiError to handle errors
        print(f'Email: {email}, Password: {password}')
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            print(res)
            return redirect(url_for("success"))
        except AuthApiError as e:
            print(e)
            return render_template("login.html", message="Invalid credentials")
    return render_template("login.html")



@app.route("/success")
def success():
    return render_template("success.html")


# on logout, redirect to logout page
@app.route("/logout", methods=["GET"])
@app.route("/logout", methods=["GET"])
def logout():
    res = supabase.auth.sign_out()
    print(res)
    return jsonify({"message": "Logout successful"})
if __name__ == "__main__":
    app.run(debug=True)
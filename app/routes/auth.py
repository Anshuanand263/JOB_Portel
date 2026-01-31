from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import get_users_col,get_providers_col


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    users_col=get_users_col()
    providers_col=get_providers_col()
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        if password != confirm_password:
            return "Passwords do not match"
        
        if users_col.find_one({"email": email}) or providers_col.find_one({"email": email}):
            return "Email already registered"

        hashed_password = generate_password_hash(password)

        data = {
            "fullname": fullname,
            "email": email,
            "password": hashed_password,
            "role": role
        }

        if role == "users":
            users_col.insert_one(data)
        else:
            providers_col.insert_one(data)

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    users_col=get_users_col()
    providers_col=get_providers_col()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        collection = users_col if role == "users" else providers_col
        user = collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user"] = user["email"]
            session["role"] = user["role"]
            session["name"] = user["fullname"]

            return redirect(url_for("users.home" if role == "users" else "providers.p_home"))

        return "Invalid email or password"

    if "user" in session:
        return redirect(url_for("users.home" if session["role"] == "users" else "providers.p_home"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

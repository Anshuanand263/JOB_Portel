from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models import get_users_col


common_bp = Blueprint("common", __name__)

@common_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    users_col=get_users_col()
    user_data = users_col.find({})
    return render_template("profile.html", user_data=user_data)


@common_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return f"{session['role']} Dashboard"


@common_bp.route("/about")
def about():
    return render_template("about.html")


@common_bp.route("/contact")
def contact():
    return render_template("contact.html")

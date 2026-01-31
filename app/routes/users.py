from flask import Blueprint, render_template, request, redirect, url_for, session
from bson import ObjectId
from ..models import get_job_collections,get_applicants_col


users_bp = Blueprint("users", __name__)

@users_bp.route("/home", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    job_collections=get_job_collections()
    if request.method == "POST":
        title = request.form.get("title")
        location = request.form.get("location")

        query = {"$or": []}
        if title:
            query["$or"].append({"title": title})
        if location:
            query["$or"].append({"location": location})
        if not query["$or"]:
            query = {}
        
        
        jobs = job_collections.find(query)
        count = job_collections.count_documents(query)

        return render_template("users/job_listing.html", jobs=jobs, counts=count)

    titles = job_collections.distinct("title")
    locations = job_collections.distinct("location")
    return render_template("users/home.html", titles=titles, locations=locations)


@users_bp.route("/users/job_listing")
def job_listing():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    job_collections=get_job_collections()
    
    jobs = job_collections.find({})
    count = job_collections.count_documents({})
    return render_template("users/job_listing.html", jobs=jobs, counts=count)


@users_bp.route("/users/job/<id>", methods=["GET", "POST"])
def job_details(id):
    if "user" not in session:
        return redirect(url_for("auth.login"))
    job_collections=get_job_collections()
    applicants_col=get_applicants_col()
    job = job_collections.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        applicants_col.insert_one({
            "company": job["company"],
            "user_name": session["name"],
            "user_email": session["user"],
            "status": "Applied"
        })
        return redirect(url_for("users.job_listing"))

    return render_template("users/job_details.html", job=job)

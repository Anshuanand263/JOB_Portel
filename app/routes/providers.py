from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from ..models import get_job_collections,get_applicants_col


providers_bp = Blueprint("providers", __name__, url_prefix="/providers")

@providers_bp.route("/home")
def p_home():
    job_collections=get_job_collections()
    
    if "user" not in session:
        return redirect(url_for("auth.login"))

    jobs = list(job_collections.find({"company": session["name"]}))
    return render_template(
        "providers/home.html",
        jobs=jobs,
        total_jobs=len(jobs),
        total_applications=20,
        active_jobs=67
    )


@providers_bp.route("/addjob", methods=["GET", "POST"])
def addjob():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        last_date = datetime.strptime(request.form.get("last_date"), "%Y-%m-%d")
        job_collections=get_job_collections()
        
        job_collections.insert_one({
            "company": session["name"],
            "title": request.form.get("title"),
            "location": request.form.get("location"),
            "job_type": request.form.get("job_type"),
            "salary": request.form.get("salary"),
            "last_date": last_date,
            "description": request.form.get("description"),
            "post_at": datetime.utcnow()
        })
        return redirect(url_for("providers.p_home"))

    return render_template("providers/addjob.html")


@providers_bp.route("/check_application")
def check_application():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    applicants_col=get_applicants_col()
    jobs = applicants_col.find({"company": session["name"]})
    return render_template("providers/check_application.html", jobs=jobs)

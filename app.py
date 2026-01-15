from flask import Flask,render_template,request,session,redirect,url_for,Response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["job_portal"]
users_col = db["users"]
providers_col = db["providers"]
job_collections = db["job_collections"]
applicants_col = db["applicants_col"]

app = Flask(__name__)
app.secret_key="oisjffkgdofg"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        if password != confirm_password:
            return "Passwords do not match"

        existing_user = users_col.find_one({"email": email})
        if existing_user:
            return "Email already registered"

        hashed_password = generate_password_hash(password)
        if role=="users":
              users_col.insert_one({
            "fullname": fullname,
            "email": email,
            "password": hashed_password,
            "role": role
        })
        else:
              providers_col.insert_one({
            "fullname": fullname,
            "email": email,
            "password": hashed_password,
            "role": role
        })
      

        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        
        if role=="users":
            user = users_col.find_one({"email": email})
            if user and check_password_hash(user["password"], password):
                
                session["user"] = user["email"]
                session["role"] = user["role"]
                session["name"] = user["fullname"]
                return redirect(url_for("home"))
            else:
                return "Invalid email or password"          
        else:
            puser = providers_col.find_one({"email": email})
            if puser and check_password_hash(puser["password"], password):
                
                session["user"] = puser["email"]
                session["role"] = puser["role"]
                session["name"] = puser["fullname"]
                return redirect(url_for("p_home"))
            else:
                return "Invalid email or password"          
    if "user" in session:
        role = session["role"]
        if role=="users":
            return redirect(url_for('home'))
        else:
            return redirect(url_for('p_home'))        
    return render_template("login.html")
#provider backend
@app.route("/providers/home")
def p_home():
    if "user" not in session:
        return redirect(url_for("login"))

    jobs = list(db.job_collections.find({"company": session["name"]}))

    total_jobs = len(jobs)
    # total_applications = sum(job.get("application_count", 0) for job in jobs)
    # active_jobs = sum(1 for job in jobs if job.get("status") == "active")

    return render_template(
        "providers/home.html",
        jobs=jobs,
        total_jobs=total_jobs,
        total_applications=20,
        active_jobs=67
    )
from datetime import datetime

@app.route("/providers/addjob",methods=["GET", "POST"])
def addjob():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method=="POST":
            
            title=request.form.get("title")
            location=request.form.get("location")
            job_type=request.form.get("job_type")
            salary=request.form.get("salary")
            last_date=request.form.get("last_date")
            description=request.form.get("description")
            last_date_str = request.form.get("last_date")
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")

 

            job_collections.insert_one({
            "company":session["name"],
            "title":title,
             "location":location,
            "job_type":job_type,
              "salary":salary,
              "last_date":last_date,
             "description":description,
              "post_at": datetime.utcnow() 
             }) 
            return redirect(url_for('p_home'))
        
    return render_template("providers/addjob.html")
    

@app.route("/providers/check_application")
def check_application():
    if "user" not in session:
        return redirect(url_for("login"))
    jobs = db.applicants_col.find({"company":session["name"]})
    return render_template("providers/check_applicatio.html",jobs=jobs)
#user backend
@app.route("/home", methods=["GET","POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method=="POST":
        title=request.form.get("title")        
        location=request.form.get("location")
        query = {"$or": []}

        if title:
           query["$or"].append({"title": title})

        if location:
           query["$or"].append({"location": location})

        if not query["$or"]:
           query = {}

        jobs = db.job_collections.find(query)
        count = db.job_collections.count_documents(query)    

        return render_template('users/job_listing.html',jobs=jobs,counts=count)        
    
    titles=db.job_collections.distinct("title")
    locations = db.job_collections.distinct("location")
    return render_template('users/index.html',titles=titles,locations=locations)
@app.route("/users/job_listing")
def job_listing():
    if "user" not in session:
        return redirect(url_for("login"))
    jobs = db.job_collections.find({})
    count = db.job_collections.count_documents({})
    return render_template('users/job_listing.html',jobs=jobs,counts=count)
@app.route('/users/job/<id>',methods=["GET","POST"])
def job_details(id):
    if "user" not in session:
        return redirect(url_for("login"))
    job = db.job_collections.find_one({"_id": ObjectId(id)})
    if request.method=="POST":           
        applicants_col.insert_one({
                 "company":job["company"],
                 "user_name":session["name"],
                 "user_email":session["user"],
                 "status":"Applied"
            })
        return redirect(url_for('job_listing'))
    return render_template('users/job_details.html',
                           job=job
                           )
# common backend
@app.route("/profile",methods=["GET","POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method=="POST":
        email=request.form.get("email")
        user_data = db.users_col.find({})
        return render_template("profile.html",user_data=user_data)
    
    return render_template("profile.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"{session['role']} Dashboard"
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)


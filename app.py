from flask import Flask,render_template,request,session,redirect,url_for,Response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["job_portal"]
users_col = db["users"]

app = Flask(__name__)
app.secret_key="oisjffkgdofg"

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        # basic validation
        if password != confirm_password:
            return "Passwords do not match"

        # check if user already exists
        existing_user = users_col.find_one({"email": email})
        if existing_user:
            return "Email already registered"

        # hash password
        hashed_password = generate_password_hash(password)

        # insert user
        users_col.insert_one({
            "fullname": fullname,
            "email": email,
            "password": hashed_password,
            "role": role
        })

        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users_col.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user"] = user["email"]
            session["role"] = user["role"]
            session["name"] = user["fullname"]
            return redirect(url_for("home"))
        else:
            return "Invalid email or password"

    return render_template("login.html")


@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Profile Page for {session['user']} ({session['role']})"


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"{session['role']} Dashboard"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/job_listing")
def job_listing():
    return render_template('job_listing.html')
@app.route('/job/<id>')
def job_details(id):
    return render_template('job_details.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')


if __name__=="__main__":
    app.run(debug=True)


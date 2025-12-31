from flask import Flask,render_template,request,session,redirect,url_for,Response

app = Flask(__name__)
app.secret_key="oisjffkgdofg"

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # handle registration
        pass
    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if email == "abc@gmail.com" and password == "123":
            session["user"] = email
            session["role"] = role
            return redirect(url_for("home"))
        else:
            return "Invalid credentials", 401

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


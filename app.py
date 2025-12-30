from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
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
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/elements')
def elements():
    return render_template('elements.html')


if __name__=="__main__":
    app.run(debug=True)


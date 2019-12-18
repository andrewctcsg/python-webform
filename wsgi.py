from flask import Flask, render_template, flash, redirect, url_for, request
from localforms import Form
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['formsdb']
collection = db["formsc"]
posts = db.posts
dup = '0'
data = []
application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def front():
    global db
    global dup
    dup = '0'
    if request.method == "POST":
        new_firstname = request.form.get("first-name", "")
        new_lastname = request.form.get("last-name", "")
        new_email = request.form.get("email", "")
        new_mobile = request.form.get("mobile", "")

        if db.posts.count_documents({}) == 0:
            new_form = Form(new_firstname, new_lastname, new_email, new_mobile)
            data.append(new_form)  # insert to ram
            db.posts.insert_one(new_form.databasepacking())  # insert to mongodb
            print("saved")
            return redirect(url_for("success"))

        for entry in db.posts.find({}):
            if new_email == entry.get('_id'):
                print("email already used")
                dup = '1'
                break
            else:
                new_form = Form(new_firstname, new_lastname, new_email, new_mobile)
                data.append(new_form)   #insert to ram
                db.posts.insert_one(new_form.databasepacking())     #insert to mongodb
                print("saved")
                dup = '0'
                return redirect(url_for("success"))
    return render_template("form.html", title='welcome', dup=dup)


@application.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == "POST":
        return redirect(url_for("front"))
    return render_template('success.html', title='success', firstn=data[-1])


@application.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == "POST":
        global data
        data = []
    return render_template('results.html', title='results', data=data)

@application.route('/resultsdb', methods=['GET', 'POST'])
def resultsdb():
    global db
    data2 = []

    for entry in db.posts.find({}):
        test = Form(entry.get('first_name'), entry.get('last_name'), entry.get('_id'), entry.get('mobile'))
        data2.append(test)

    if request.method == "POST":
        for index in range(db.posts.count_documents({})):
            print(posts.count_documents({}))
            db.posts.delete_one({})
        data2 = []
    return render_template('resultsdb.html', title='resultsdb', data=data2)

if __name__ == "__main__":
    application.run(debug=True)

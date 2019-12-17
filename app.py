from flask import Flask, render_template, flash, redirect, url_for, request
from localforms import Form

data = []
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def front():
    if request.method == "POST":
        new_firstname = request.form.get("first-name", "")
        new_lastname = request.form.get("last-name", "")
        new_email = request.form.get("email", "")
        new_mobile = request.form.get("mobile", "")

        new_form = Form(new_firstname, new_lastname, new_email, new_mobile)
        data.append(new_form)

        return redirect(url_for("success"))
    return render_template("form.html", title='welcome')


@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == "POST":
        return redirect(url_for("front"))
    return render_template('success.html', title='success', firstn=data[-1])


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == "POST":
        global data
        data = []
    return render_template('results.html', title='success', data=data)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask
from datetime import datetime
import os
from flask import render_template, request, session, redirect, url_for, flash
from forms import MyForm
from loguru import logger

app  = Flask(__name__)
app.config['SECRET_KEY'] = 'lkfdlkvskds'
logger.add("logs.log")

menu = {
            "/": "Home",
            "/about": "About me",
            "/certifications": "My licenses & certifications",
            "/contact": "Contact"
        }

@app.route('/')
def index():
    return render_template("main.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/about")
def about():
    return render_template("about.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/certifications")
def certifications():
    return render_template("certifications.html", menu=menu,
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@app.route("/portfolio")
def portfolio():
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MyForm()
    if form.validate_on_submit():
        message = get_log_message(form)
        logger.info(message)
        session['name'] = form.name.data
        session['email'] = form.email.data        
        flash(f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))
    elif request.method == 'POST':
        flash("Post method validation failed", category = 'warning')
        return render_template('contact.html', menu=menu, form=form)

    form.name.data = session.get("name")
    form.email.data = session.get("email")
    return render_template('contact.html', menu=menu, form=form)

@app.route('/delete-user-data')
def delete_user_data():
    session.pop("email", default=None)
    session.pop("name", default=None)
    return redirect(url_for("contact"))

def get_log_message(form):
    fields = (
        form.name.data,
        form.email.data,
        form.phone.data,
        form.subject.data,
        form.message.data
    )
    return " ".join(fields)

if __name__ == '__main__':
    app.run(debug=True)
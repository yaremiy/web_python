from flask import Flask
from datetime import datetime
import os
from flask import render_template, request, session, redirect, url_for, flash
from app.forms import MyForm, LoginForm, RegistrationForm
from loguru import logger
from app import app, db
from app.models import Message, User


logger.add("logs.log")

menu = {
    "/": "Home",
    "/about": "About me",
    "/certifications": "My licenses & certifications",
    "/contact": "Contact",
    "/login": "Login",
    "/register": "Regeser"
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
        logger.info(get_log_message(form))
        subject = dict(form.subject.choices).get(form.subject.data)
        session['name'] = form.name.data
        session['email'] = form.email.data
        message = Message(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=subject,
            message=form.message.data
        )
        try:
            db.session.add(message)
            db.session.commit()
        except:
            db.session.flush()
            db.session.rollback()
        flash(
            f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))
    elif request.method == 'POST':
        flash("Post method validation failed", category='warning')
        return render_template('contact.html', menu=menu, form=form)

    form.name.data = session.get("name")
    form.email.data = session.get("email")
    return render_template('contact.html', menu=menu, form=form)



def get_log_message(form):
    fields = (
        form.name.data,
        form.email.data,
        form.phone.data,
        form.subject.data,
        form.message.data
    )
    return " ".join(fields)


@app.route('/delete-message/<id>')
def delete_message(id):
    Message.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("messages"))


@app.route('/messages')
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages, menu=menu)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash(
                f"Account created for {form.username.data}!", category='success')
            return redirect(url_for("login"))
        except:
            db.session.flush()
            db.session.rollback()

    return render_template('register.html', menu=menu, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            return redirect(url_for("index"))
        else:
            flash(f"Email or password is incorrect", category='danger')
    return render_template('login.html', menu=menu, form=form)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', menu=menu, users=users)


@app.route('/delete-user/<id>')
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("users"))


if __name__ == '__main__':
    app.run(debug=True)

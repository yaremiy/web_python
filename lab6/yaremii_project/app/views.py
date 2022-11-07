from flask import Flask
from datetime import datetime
import os
from flask import render_template, request, session, redirect, url_for, flash
from app.forms import MyForm
from loguru import logger
from app import app, db
from app.models import Message


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
        logger.info(get_log_message(form))
        session['name'] = form.name.data
        session['email'] = form.email.data    
        message = Message(
            name = form.name.data,
            email = form.email.data,
            phone = form.phone.data,
            subject = form.subject.data,
            message = form.message.data
        )
        db.session.add(message)
        db.session.commit()    
        flash(f"Your message has been sent: {form.name.data}, {form.email.data}", category='success')
        return redirect(url_for("contact"))
    elif request.method == 'POST':
        flash("Post method validation failed", category = 'warning')
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

if __name__ == '__main__':
    app.run(debug=True)
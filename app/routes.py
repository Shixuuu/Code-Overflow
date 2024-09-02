from app import app
from flask import render_template, request, redirect, url_for,flash
from app.models import User, db
from app.form import RegistrationForm, LoginForm

@app.route('/')
def home():
    # Default form type
    form_type = request.args.get('form_type', 'login')
    
    if form_type == 'signup':
        form = RegistrationForm()
    else:
        form = LoginForm()
    
    return render_template('home.html', form_type=form_type, form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    print("Form method:", request.method)  # Debugging line
    if form.validate_on_submit():
        print("Form is valid")  # Debugging line
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Congratulations, you are now registered!')
            return redirect(url_for('home', form_type='login'))
        else:
            flash('User already exists. Please login.')
            return redirect(url_for('home', form_type='login'))
    else:
        print("Form errors:", form.errors)  # Debugging line
    return render_template('home.html', form=form)
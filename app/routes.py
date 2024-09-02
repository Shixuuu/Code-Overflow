from app import app
from flask import render_template, request, redirect, url_for,flash,get_flashed_messages    
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
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Congratulations, you are now registered!', 'success')
            return redirect(url_for('home', form_type='login'))
        else:
            flash('Username is already taken, please choose a different username.', 'signuperror')
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'signuperror')
    print(get_flashed_messages(with_categories=True))  # Debug print statement
    return render_template('home.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            return redirect(url_for('uh'))
        else:
            flash('Invalid username or password.', 'loginerror')
    print(get_flashed_messages(with_categories=True))  # Debug print statement
    return render_template('home.html', form=form)
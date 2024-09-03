from app import app
from flask import render_template, request, redirect, url_for,flash,session
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
    
    return render_template('signinpage.html', form_type=form_type, form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now registered!', 'success')
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'signuperror')
    return render_template('signinpage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id  # Store user_id in session
            if user.first_login:
                return redirect(url_for('personalized_questions', user_id=user.id))
            else:
                return redirect(url_for('homepage'))
        else:
            flash('Invalid username or password.', 'loginerror')
    return render_template('signinpage.html', form=form)
@app.route('/personalized_questions/<int:user_id>', methods=['GET', 'POST'])
def personalized_questions(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        sector = request.form.get('sector')
        if sector:
            user.sector = sector
            user.first_login = False
            db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('whenin/personalized_questions.html', user=user)

@app.route('/homepage')
def homepage():
    user_id = session.get('user_id')  # Assuming user_id is stored in session
    if user_id:
        user = User.query.get(user_id)
        return render_template('whenin/homepage.html', user=user)
    else:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in
@app.route('/social')
def social():
    return render_template('whenin/social.html') 
@app.route('/insurance')
def insurance():
    return render_template('whenin/insurance.html')
@app.route('/investment')
def investment():
    return render_template('whenin/investment.html')
@app.route('/loaning')
def loaning():
    return render_template('whenin/loaning.html')    

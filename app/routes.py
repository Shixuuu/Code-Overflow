from app import app
from flask import render_template, request, redirect, url_for,flash,session ,jsonify
from app.models import User, Friend, FriendRequest,db
from app.form import RegistrationForm, LoginForm


def make_everyone_friends():
    users = User.query.all()
    for user in users:
        for friend in users:
            if user.id != friend.id:
                # Check if the friendship already exists
                existing_friendship = Friend.query.filter_by(user_id=user.id, friend_id=friend.id).first()
                if not existing_friendship:
                    new_friend = Friend(user_id=user.id, friend_id=friend.id, friend_name=friend.username, friend_image="path/to/default/image.jpg")
                    db.session.add(new_friend)
                    print(f"Added {friend.username} as friend to {user.username}")
    db.session.commit()
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


@app.route('/friends/<int:user_id>')
def friends(user_id):
    user = User.query.get(user_id)
    if user:
        friends = Friend.query.filter_by(user_id=user_id).all()
        friends_data = [{
            'id': friend.friend_id,  # Assuming 'friend_id' corresponds to the friend's ID
            'name': friend.friend_name,
            'money': User.query.get(friend.friend_id).money  # Assuming 'money' is a field in User model
        } for friend in friends]
        return render_template('whenin/loaning.html', user=user,  friends=friends_data, user_id=user_id)
    else:
        return "User not found", 404

@app.route('/make_friends')
def make_friends():
    make_everyone_friends()
    return "All users are now friends with each other!"

@app.route('/homepage')
def homepage():
    user_id = session.get('user_id')
    return render_template('whenin/homepage.html', user_id=user_id)

@app.route('/investment', methods=['GET', 'POST'])
def investment():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if request.method == 'POST':
            sector = request.form.get('sector')
            # Process the sector data as needed
            flash('Sector preference saved!', 'success')
        if 'first_investment_visit' not in session:
            session['first_investment_visit'] = True
            flash('Welcome to the investment page!', 'firstvisit')
        return render_template('whenin/investment.html', user=user, user_id=user_id)
    else:
        return redirect(url_for('login'))
@app.route('/insurance')
def insurance():
    user_id = session.get('user_id')
    return render_template('whenin/insurance.html', user_id=user_id)

@app.route('/social')
def social():
    user_id = session.get('user_id')
    friend_requests = []
    friends = []
    if user_id:
        # Retrieve friend requests where receiver_id matches the current user's ID
        friend_requests = FriendRequest.query.filter_by(receiver_id=user_id).all()
        friend_requests = [request.to_dict() for request in friend_requests]

        # Retrieve friends where user_id matches the current user's ID
        friends = Friend.query.filter_by(user_id=user_id).all()
        friends = [{
            'id': friend.id,
            'user_id': friend.user_id,
            'friend_id': friend.friend_id,
            'friend_name': friend.friend_name,
            # 'friend_image': friend.friend_image,
            'friend_money': User.query.get(friend.friend_id).money  # Assuming 'money' is a field in User model
        } for friend in friends]

    return render_template('whenin/social.html', user_id=user_id, friend_requests=friend_requests, friends=friends)

@app.route('/loaning/<int:user_id>')
def loaning(user_id):
    user = User.query.get(user_id)
    if user:
        friends = Friend.query.filter_by(user_id=user_id).all()
        friends_data = [{
            'id': friend.friend_id,  # Assuming 'friend_id' corresponds to the friend's ID
            'name': friend.friend_name,
            'money': User.query.get(friend.friend_id).money  # Assuming 'money' is a field in User model
        } for friend in friends]
        return render_template('whenin/loaning.html', user=user, friends=friends_data, user_id=user_id)
    else:
        return "User not found", 404

@app.route('/friend_requests')
def friend_requests():
    current_user_id = session.get('user_id')
    if current_user_id:
        friend_requests = FriendRequest.query.filter_by(receiver_id=current_user_id).all()
        return render_template('whenin/friendReq.html', friend_requests=friend_requests)
    return redirect(url_for('login'))


@app.route('/add_friend/<int:user_id>', methods=['POST'])
def add_friend(user_id):
    current_user_id = session.get('user_id')
    if current_user_id:
        user = User.query.get(user_id)
        if user:
            # Check if a friend request already exists
            existing_request = FriendRequest.query.filter_by(sender_id=current_user_id, receiver_id=user.id).first()
            if not existing_request:
                # Create a new friend request
                new_request = FriendRequest(sender_id=current_user_id, receiver_id=user.id)
                db.session.add(new_request)
                db.session.commit()
                flash('Friend request sent!', 'success')
            else:
                flash('Friend request already sent.', 'info')
        else:
            flash('User does not exist.', 'danger')
    return redirect(url_for('search_and_send_request'))

@app.route('/accept_friend_request/<int:request_id>', methods=['POST'])
def accept_friend_request(request_id):
    friend_request = FriendRequest.query.get(request_id)
    if friend_request:
        # Create a friendship entry for the receiver
        new_friend_receiver = Friend(
            user_id=friend_request.receiver_id,
            friend_id=friend_request.sender_id,
            friend_name=friend_request.sender.username,
            # friend_image=friend_request.sender.profile_image  # Assuming profile_image is a field in User model
        )
        db.session.add(new_friend_receiver)

        # Create a friendship entry for the sender
        new_friend_sender = Friend(
            user_id=friend_request.sender_id,
            friend_id=friend_request.receiver_id,
            friend_name=friend_request.receiver.username,
            # friend_image=friend_request.receiver.profile_image  # Assuming profile_image is a field in User model
        )
        db.session.add(new_friend_sender)

        # Delete the friend request
        db.session.delete(friend_request)
        db.session.commit()
        flash('Friend request accepted!', 'success')
    return redirect(url_for('social'))

@app.route('/decline_friend_request/<int:request_id>', methods=['POST'])
def decline_friend_request(request_id):
    friend_request = FriendRequest.query.get(request_id)
    if friend_request:
        db.session.delete(friend_request)
        db.session.commit()
        flash('Friend request declined!', 'success')
    return redirect(url_for('friend_requests'))
# app/routes.py
@app.route('/search_friends', methods=['POST'])
def search_friends():
    query = request.form.get('q')
    if query:
        users = User.query.filter(User.username.contains(query)).all()
        return render_template('whenin/social.html', users=users)
    return redirect(url_for('social'))

@app.route('/search_and_send_request', methods=['POST'])
def search_and_send_request():
    query = request.form.get('q')
    current_user_id = session.get('user_id')
    response = {}

    if query and current_user_id:
        user = User.query.filter(User.username.contains(query)).first()
        if user:
            if user.id == current_user_id:
                response['message'] = 'You cannot send a friend request to yourself.'
                response['status'] = 'danger'
            else:
                # Check if the users are already friends
                existing_friendship = Friend.query.filter_by(user_id=current_user_id, friend_id=user.id).first()
                if existing_friendship:
                    response['message'] = 'You are already friends with this user.'
                    response['status'] = 'info'
                else:
                    # Check if a friend request already exists
                    existing_request = FriendRequest.query.filter_by(sender_id=current_user_id, receiver_id=user.id).first()
                    if existing_request:
                        response['message'] = 'Friend request already sent.'
                        response['status'] = 'info'
                    else:
                        # Check if there is a pending friend request from the other user
                        pending_request = FriendRequest.query.filter_by(sender_id=user.id, receiver_id=current_user_id).first()
                        if pending_request:
                            response['message'] = 'There is already a pending friend request from this user.'
                            response['status'] = 'info'
                        else:
                            # Create a new friend request
                            new_request = FriendRequest(sender_id=current_user_id, receiver_id=user.id)
                            db.session.add(new_request)
                            db.session.commit()
                            response['message'] = 'Friend request sent!'
                            response['status'] = 'success'
        else:
            response['message'] = 'User does not exist.'
            response['status'] = 'danger'
    else:
        response['message'] = 'Invalid query.'
        response['status'] = 'danger'

    return jsonify(response)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user, user_id=user_id)
    else:
        return "User not found", 404
    
@app.route('/loan', methods=['POST'])
def loan():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not logged in'})

    data = request.get_json()
    friend_id = data.get('friend_id')
    loan_amount = data.get('loan_amount')

    if not friend_id or not loan_amount:
        return jsonify({'success': False, 'message': 'Invalid data'})

    lender = User.query.get(user_id)
    borrower = User.query.get(friend_id)

    if not lender:
        print(f"Lender with user_id {user_id} not found")
    if not borrower:
        print(f"Borrower with friend_id {friend_id} not found")

    if not lender or not borrower:
        return jsonify({'success': False, 'message': 'User not found'})

    # Update the money fields
    lender.money -= int(loan_amount)
    borrower.money += int(loan_amount)

    # Update the User class instead of creating a new Loan entry
    db.session.commit()

    return jsonify({'success': True})
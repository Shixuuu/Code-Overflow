from app import app

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        from app.models import db
        db.create_all()
    
    # Run the app

    app.run(debug=True)

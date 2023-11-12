
from functions import search, db, authenticate_user
from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils import *

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if authenticate_user(email, password):
            # Authentication succeeded, redirect to index.html
            return redirect(url_for('search_flask'))
        else:
            # Authentication failed, display an error message or redirect to login page
            return render_template('login.html', error_message='Invalid email or password')
    # Render the login page for GET requests
    return render_template('login.html', error_message=None)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user data from the registration form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        cuisines = request.form.getlist('cuisine')
        # Store user data in the "users" collection
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'cuisine': cuisines
        }
        # Save user data to MongoDB
        db.users.insert_one(user_data)
        # Redirect to the /login endpoint
        return redirect(url_for('login'))
    return render_template('registration.html')  # Render the registration page


@app.route('/search', methods=['GET'])
def search_flask():
    search_term = request.args.get('query')
    if search_term:
        results = search(search_term)
        return jsonify(results)
        # Redirect to index.html if no search term is provided
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

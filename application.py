from functions import search, db
from flask import Flask, render_template, request, redirect, url_for
from utils import *

app = Flask(__name__)


@app.route('/')
def registration_page():
    return render_template('registration.html')

@app.route('/index')
def index():
    return render_template('index.html')
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
        return redirect(url_for('index'))

@app.route('/search')
def search_flask():
    search_term = request.args.get('query')
    return create_response(search(search_term))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

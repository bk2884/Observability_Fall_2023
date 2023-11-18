from flask import Flask, render_template, request, redirect, url_for, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from functions import search, db, authenticate_user
from prometheus_flask_exporter import Counter

app = Flask(__name__)

# Or use ELASTIC_APM in your application's settings
from elasticapm.contrib.flask import ElasticAPM
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'my-service-name',

  'SECRET_TOKEN': 'aRMKjDPld9ZjkZRof9',

  'SERVER_URL': 'https://f17ae4172ef741c1aadac9f2de418507.apm.us-east-2.aws.elastic-cloud.com:443',

  'ENVIRONMENT': 'my-environment',
}

apm = ElasticAPM(app)
metrics = PrometheusMetrics(app)  # Initialize Prometheus Metrics

login_attempts = Counter('login_attempts', 'Number of login attempts')
registrations = Counter('registrations', 'Number of user registrations')
search_queries = Counter('search_queries', 'Number of search queries')


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_attempts.inc()  # Increment login attempts counter
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
        registrations.inc()  # Increment registrations counter
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
        search_queries.inc()  # Increment search queries counter
        results = search(search_term)
        return jsonify(results)
        # Redirect to index.html if no search term is provided
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

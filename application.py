from flask import Flask, render_template, request, redirect, url_for, jsonify
from prometheus_flask_exporter import PrometheusMetrics, Counter
from functions import search, db, authenticate_user
from elasticapm.contrib.flask import ElasticAPM
from elasticapm import capture_span, get_trace_id, get_transaction_id, get_span_id
import logging
from ecs_logging import StdlibFormatter
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Elastic APM configuration
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'my-service-name',
  'SECRET_TOKEN': 'aRMKjDPld9ZjkZRof9',
  'SERVER_URL': 'https://f17ae4172ef741c1aadac9f2de418507.apm.us-east-2.aws.elastic-cloud.com:443',
  'ENVIRONMENT': 'my-environment',
}

apm = ElasticAPM(app)
metrics = PrometheusMetrics(app)

logger = logging.getLogger('ecs_logger')
logger.setLevel(logging.INFO)
log_file_path = 'app.log'
file_handler = RotatingFileHandler(log_file_path, maxBytes=1000000, backupCount=5)
formatter = StdlibFormatter()
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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
        with capture_span('search_operation', 'custom', labels={'search_term': search_term}):
            trace_id = get_trace_id()
            transaction_id = get_transaction_id()
            span_id = get_span_id()

            logger.info(f"Search operation - Trace ID: {trace_id}, Transaction ID: {transaction_id}, Span ID: {span_id}")

            search_queries.inc()
            results = search(search_term)
            return jsonify(results)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

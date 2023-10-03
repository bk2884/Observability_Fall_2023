from functions import search
from flask import Flask, render_template, request
from utils import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_flask():
    search_term = request.args.get('query')
    return create_response(search(search_term))

if __name__ == '__main__':
    app.run(debug=True)
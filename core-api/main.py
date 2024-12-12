from flask import Flask, jsonify, render_template, request
from recommendation_agent import generate_payload, recommend
import os

app = Flask(__name__, template_folder=os.path.join('..', 'web-app'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result_page', methods=['POST'])
def result_page():
    # Get form data
    username = request.form.get('username')
    job_title = request.form.get('job-title')
    searches = request.form.get('searches')
    products = request.form.getlist('products')

    # Generate payload
    search_queries = searches.split(',')
    payload = generate_payload(job_title, products[0], search_queries)

    # Get recommendations
    recommendations = recommend(payload)

    # Pass these variables to the template
    return render_template('Result_page.html', username=username, job_title=job_title, searches=searches, products=products, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
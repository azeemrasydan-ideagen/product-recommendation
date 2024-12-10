from flask import Flask, jsonify
from recommendation_agent import recommend, payload

app = Flask(__name__)

@app.route('/main_code', methods=['GET'])

def main_code():
    #Whatever code plus api that the project needs
    payload()
    recommend(payload)
    return jsonify({'message': 'Hello from main code!'})

if __name__ == '__main__':
    app.run(debug=True)
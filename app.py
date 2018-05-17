from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'Message': 'Hello, World!'})

@app.route('/hello')
def hello():
    return jsonify({'Message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=False)

# app.py
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from auth import auth  # Import the auth blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize bcrypt for password hashing
bcrypt = Bcrypt(app)

# Register the auth blueprint
app.register_blueprint(auth, url_prefix='/auth')  # All routes will have '/auth' prefix

# Home route for testing
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the authentication API'})

if __name__ == '__main__':
    app.run(debug=True)

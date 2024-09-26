from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from auth import auth  # Import the auth blueprint
from chat import chat_bp, socketio  # Import the chat module
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize bcrypt for password hashing
bcrypt = Bcrypt(app)

# Register the auth blueprint
app.register_blueprint(auth, url_prefix='/auth')  # All routes will have '/auth' prefix

# Register the chat blueprint
app.register_blueprint(chat_bp, url_prefix='/chat')  # All routes will have '/chat' prefix

# Initialize SocketIO
socketio.init_app(app)

# Home route for testing
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the authentication and chat API'})

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Use socketio.run instead of app.run

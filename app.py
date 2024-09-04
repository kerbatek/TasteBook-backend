# app.py
from flask import Flask
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)  # This will allow all origins by default

# Import routes after app initialization
from routes import users

# Register Blueprint
app.register_blueprint(users)

if __name__ == '__main__':
    app.run(debug=True)

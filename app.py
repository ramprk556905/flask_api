import os
from flask import Flask, request, jsonify
from extensions import db, login_manager
from flasgger import Swagger
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__)
swagger = Swagger(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:ramprk97@localhost:5432/blog-post')

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Post  # Import models after initializing db to avoid circular imports

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Your routes here...

if __name__ == "__main__":
    app.run(debug=True)

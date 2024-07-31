from flask import Flask
from extensions import db, login_manager
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ramprk97@localhost:5432/blog-post'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from routes import *  # Import routes after initializing app to avoid circular imports

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)

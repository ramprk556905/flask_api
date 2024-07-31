from flask import request, jsonify
from app import app, db
from models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/register', methods=['POST'])
def register():
    """
    User registration.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      201:
        description: Registration successful
      400:
        description: Username already exists
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    User login.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            user_id:
              type: integer
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/posts', methods=['GET'])
@login_required
def get_posts():
    """
    Get all posts.
    ---
    responses:
      200:
        description: List of posts
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              content:
                type: string
              user_id:
                type: integer
    """
    posts = Post.query.all()
    posts_list = [{'id': p.id, 'title': p.title, 'content': p.content, 'user_id': p.user_id} for p in posts]
    return jsonify(posts_list), 200

@app.route('/posts', methods=['POST'])
@login_required
def create_post():
    """
    Create a new post.
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: content
        in: formData
        type: string
        required: true
    responses:
      201:
        description: Post created successfully
      400:
        description: Invalid user
    """
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = current_user.id

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Invalid user'}), 400

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

import bcrypt
import datetime
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import json
import os
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS 
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_sslify import SSLify
app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = 'img'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Настройка JWT-модуля

sslify = SSLify(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Установите свой секретный ключ
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
    



users = load_data('users.json')


@app.route('/authenticate', methods=['POST'])
def authenticate():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  user = next((user for user in users if user['email'] == email), None)

  if user and bcrypt.check_password_hash(user['password'], password):
    access_token = create_access_token(identity={
        'email': email,
        'access_level': user['access_level']
    })
    return jsonify({'token': access_token}), 200

  return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/index', methods=['GET'])
@jwt_required()
def list_profiles():
    current_user = get_jwt_identity()
    return render_template('profiles.html', profiles = profiles, current_user = current_user)

# Функция сохранения данных в файл
def save_data():
  with open('users.json', 'w') as users_file:
    json.dump(users, users_file, indent=4)
@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  # Проверяем, что пользователь с таким email не зарегистрирован
  if next((user for user in users if user['email'] == email), None):
    return jsonify({'message':
                    'User with this email is already registered'}), 400

  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
  new_user = {
      'email': email,
      'password': hashed_password,
      'access_level': 'user'
  }
  users.append(new_user)

  save_data()  # Сохраняем данные в файл
  return jsonify({'message': 'Registration successful'}), 200



def read_posts_from_file():
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    return posts
    
@app.route('/posts', methods=['GET'])
def display_posts():
    posts = read_posts_from_file()

    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(posts)

    return render_template('posts.html', posts=posts)


@app.route('/')
def form():
    return render_template('login.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/post', methods=['POST'])
def create_post():
    try:
        title = request.form.get('title')
        text = request.form.get('text')
        photo = request.files['photo']

        posts = read_posts_from_file()
        try:
            if photo:
                filename = secure_filename(photo.filename)
                filepath = os.path.join('static', 'img', filename)
                photo.save(filepath)
            else:
                filename = None
        except (FileNotFoundError, PermissionError) as e:
            print("Error saving file:", str(e))
            return jsonify({"error": f"Error saving file: {str(e)}"}), 500

        new_post = {
            "title": title,
            "text": text,
            "photo": f"/static/img/{filename}"
        }

        with open('posts.json', 'w') as file:
            posts.append(new_post)
            json.dump(posts, file, indent=2)

        return jsonify({"message": "Post created successfully"})
    except Exception as e:
        print("Error creating post:", str(e))
        return jsonify({"error": "Error creating post"}), 500

@app.route('/post/delete', methods=['POST'])
def delete_post():
    try:
        data = request.get_json()
        post_id = data.get('post_id')

        if post_id is None:
            return jsonify({"error": "No post_id provided"}), 400

        posts = read_posts_from_file()

        data = request.get_json()
        post_id = int(data.get('post_id'))  # Convert post_id to integer

        # Then perform the comparison or any other operations
        if post_id < 0 or post_id >= len(posts):
            return jsonify({"error": "Invalid post index"}), 400

        deleted_post = posts.pop(post_id)

        # Delete associated photo if exists
        photo_path = deleted_post.get('photo')
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)

        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=2)

        return jsonify({"message": "Post deleted successfully"})
    except Exception as e:
        print("Error deleting post:", str(e))
        return jsonify({"error": "Error deleting post"}), 500


@app.route('/search', methods=['POST'])
def search_posts():
    search_term = request.json.get('search_term', '').lower()
    posts = read_posts_from_file()

    filtered_posts = [post for post in posts if search_term in post['title'].lower()]

    return jsonify(filtered_posts)



def save_profiles(data):
    with open('profiles.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

profiles = load_data('profiles.json')  
# Защищенный маршрут

@app.route('/profile/<int:profile_id>')
def view_profile(profile_id):
    profile = next((p for p in profiles if p['id'] == profile_id), None) 
    if profile:
        return render_template('profile.html', profile=profile)
    return 'Profile not found', 404

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        bio = request.form['bio']

        new_profile = {
            'id': len(profiles) + 1,
            'username': username,
            'email': email,
            'bio': bio
        }

        profiles.append(new_profile)
        save_profiles(profiles)  
        return redirect(url_for('list_profiles'))
    return render_template('create_profile.html')

@app.route('/edit_profile/<int:profile_id>', methods=['GET', 'POST'])
def edit_profile(profile_id):
    profile = next((p for p in profiles if p['id'] == profile_id), None)
    if not profile:
        return 'Profile not found', 404

    if request.method == 'POST':
        profile['username'] = request.form['username']
        profile['email'] = request.form['email']
        profile['bio'] = request.form['bio']
        save_profiles(profiles) 
        return redirect(url_for('list_profiles'))

    return render_template('edit_profile.html', profile=profile)

@app.route('/delete_profile/<int:profile_id>', methods=['POST'])
def delete_profile(profile_id):
    profile = next((p for p in profiles if p['id'] == profile_id), None)
    if not profile:
        return 'Profile not found', 404

    profiles.remove(profile)
    save_profiles(profiles)  
    return redirect(url_for('list_profiles'))

if __name__ == '__main__':
    app.run(debug=True) 

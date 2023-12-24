from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from flask_cors import CORS 
from werkzeug.utils import secure_filename
app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = 'img'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
def read_posts_from_file():
    try:
        with open('data.json', 'r') as file:
            content = file.read()
            posts = json.loads(content) if content else []
            return posts if isinstance(posts, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return []
    
@app.route('/posts', methods=['GET'])
def display_posts():
    posts = read_posts_from_file()

    if request.headers.get('Content-Type') == 'application/json':
        return jsonify(posts)

    return render_template('posts.html', posts=posts)



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
        posts.append(new_post)

        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=2)

        return jsonify({"message": "Post created successfully"})
    except Exception as e:
        print("Error creating post:", str(e))
        return jsonify({"error": "Error creating post"}), 500



@app.route('/search', methods=['POST'])
def search_posts():
    search_term = request.json.get('search_term', '').lower()
    posts = read_posts_from_file()

    filtered_posts = [post for post in posts if search_term in post['title'].lower()]

    return jsonify(filtered_posts)

@app.route('/delete-post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        posts = read_posts_from_file()

        if 0 < post_id <= len(posts):
            deleted_post = posts.pop(post_id - 1)

            with open('data.json', 'w') as file:
                json.dump(posts, file, indent=2)

            return jsonify({
                "message": "Post deleted successfully",
                "deleted_post": deleted_post
            })
        else:
            return jsonify({"error": "Invalid post ID"}), 400
    except Exception as e:
        print("Error deleting post:", str(e))
        return jsonify({"error": "Error deleting post"}), 500


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return []
    
def save_profiles(data):
    with open('profiles.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

profiles = load_data('profiles.json')  

@app.route('/')
def list_profiles():
    return render_template('profiles.html', profiles=profiles)

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

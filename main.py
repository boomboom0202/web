from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from flask_cors import CORS 
from werkzeug.utils import secure_filename
app = Flask(__name__)
CORS(app) 

client_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , 'client'))
print(client_app_path)

if not os.path.exists('images'):
    os.makedirs('images')

@app.route('/posts/create_post', methods=['POST'])
def create_post():
    try:
        file = request.files.get('file') 
        title = request.form.get('title','') 
        content = request.form.get('content','') 
        filename = None  
        
        if file: 
            filename = os.path.join(client_app_path, 'images', file.filename)
            print(filename)
            file.save(filename) 

        post_info = {
            'filename': f"images/{file.filename}",
            'title': title, 
            'content': content
        }

        existing_data = [] 
        if os.path.exists('posts.json'): 
            with open('post.json', 'r', encoding='utf-8') as file: 
                existing_data = json.load(file) 
        existing_data.append(post_info)

        with open('posts.json', 'w', encoding='utf-8') as file: 
            json.dump(existing_data, file, indent=2) 
        
        response_data = {
            'message': 'Post created successfully', 
            'filename': filename, 
            'title': title, 
            'content': content, 
        }

        return jsonify(response_data), 201 
    except Exception as e:
        error_message = str(e)
        print("Error:", error_message)  # Log the error
        response_data = {'error': error_message}
        return jsonify(response_data), 500
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return []
@app.route('/posts') 
def view_post():
    return render_template('posts.html', posts = posts)
def save_profiles(data):
    with open('profiles.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

profiles = load_data('profiles.json')  
posts = load_data('posts.json')

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

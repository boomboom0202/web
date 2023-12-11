from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_profiles():
    if os.path.exists('profiles.json'):
        with open('profiles.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        return []

def save_profiles(data):
    with open('profiles.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

profiles = load_profiles()  

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
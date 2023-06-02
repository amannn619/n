from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import User, Img
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        img_src = request.form.get('img')#Gets the note from the HTML 
        print(img_src)
        if not img_src:
            flash('Image not selected!', category='error') 
        else:
            flash('Image Uploaded!', category='success')

    return render_template("home.html", user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
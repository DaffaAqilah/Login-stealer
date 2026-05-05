from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import UserSubmission

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/form', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        box_id   = request.form.get('box_id', 0, type=int)

        if not email or not password:
            error = 'Email dan password wajib diisi.'
        else:
            entry = UserSubmission(email=email, password=password, box_id=box_id)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('auth.check_email'))

    # ambil box_id dari query param saat GET
    box_id = request.args.get('box_id', 0, type=int)
    return render_template('form.html', box_id=box_id, error=error)


@auth_bp.route('/check-email')
def check_email():
    return render_template('check_email.html')
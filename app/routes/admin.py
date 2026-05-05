from functools import wraps
from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, flash)
from app.models import AdminUser, UserSubmission
from app import db

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if AdminUser.verify(username, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        error = 'Username atau password salah.'
    return render_template('admin_login.html', error=error)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    users = UserSubmission.query.order_by(
        UserSubmission.created_at.desc()
    ).all()
    return render_template('admin_dashboard.html', users=users)


@admin_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit(user_id):
    entry = UserSubmission.query.get_or_404(user_id)
    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        if new_email:
            entry.email = new_email
            db.session.commit()
            flash('Data berhasil diperbarui.', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin_edit.html', entry=entry)


@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete(user_id):
    entry = UserSubmission.query.get_or_404(user_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Data berhasil dihapus.', 'danger')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))
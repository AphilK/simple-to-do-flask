from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db, get_current_sprint, get_all_sprints, get_sprint

bp = Blueprint('task', __name__)

@bp.route('/')
def index():
    db = get_db()

    # Get current sprint if user is logged in
    current_sprint = None
    all_sprints = []
    sprint_id = request.args.get('sprint_id', type=int)

    if g.user:
        if sprint_id:
            current_sprint = get_sprint(sprint_id)
        else:
            current_sprint = get_current_sprint(g.user['id'])
        all_sprints = get_all_sprints(g.user['id'])

    # Fetch tasks, filtered by sprint if user is logged in
    if g.user and current_sprint:
        posts = db.execute(
            'SELECT t.id, title, body, created, author_id, username, status, sprint_id'
            ' FROM task t JOIN user u ON t.author_id = u.id'
            ' WHERE t.sprint_id = ? AND t.author_id = ?'
            ' ORDER BY CASE '
            '   WHEN status = "Started" THEN 1 '
            '   WHEN status = "Developing" THEN 2 '
            '   WHEN status = "Finished" THEN 3 '
            '   ELSE 4 '
            ' END, created DESC',
            (current_sprint['id'], g.user['id'])
        ).fetchall()
    else:
        posts = db.execute(
            'SELECT t.id, title, body, created, author_id, username, status'
            ' FROM task t JOIN user u ON t.author_id = u.id'
            ' ORDER BY CASE '
            '   WHEN status = "Started" THEN 1 '
            '   WHEN status = "Developing" THEN 2 '
            '   WHEN status = "Finished" THEN 3 '
            '   ELSE 4 '
            ' END, created DESC'
        ).fetchall()

    return render_template('task/index.html', posts=posts, current_sprint=current_sprint, all_sprints=all_sprints)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            # Get current sprint for the user
            current_sprint = get_current_sprint(g.user['id'])

            db.execute(
                'INSERT INTO task (title, body, author_id, sprint_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], current_sprint['id'])
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT t.id, title, body, created, author_id, username, status, sprint_id'
        ' FROM task t JOIN user u ON t.author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('task.index'))

    return render_template('task/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('task.index'))

@bp.route('/<int:id>/status', methods=('POST',))
@login_required
def update_status(id):
    post = get_post(id)

    data = request.get_json()
    new_status = data.get('status', '').strip()

    # Validate status
    valid_statuses = ['Started', 'Developing', 'Finished']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400

    db = get_db()
    db.execute(
        'UPDATE task SET status = ? WHERE id = ?',
        (new_status, id)
    )
    db.commit()

    return jsonify({'success': True, 'status': new_status})
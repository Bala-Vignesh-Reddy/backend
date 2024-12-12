from flask import Blueprint, request, jsonify
from app.models.artifact import db_connection
import sqlite3

bp = Blueprint('artifacts', __name__, url_prefix='/artifacts')

@bp.route('/', methods=['GET'])
def get_all_artifacts():
    conn = db_connection()
    cursor = conn.cursor()

    status = request.args.get('status')
    query = "select * from artifact"
    parameters = []

    if status:
        query += " where status = ?"
        parameters.append(status)
    
    artifacts = cursor.execute(query, parameters).fetchall()
    conn.close()

    artifact_list = []
    for artifact in artifacts:
        artifact_list.append({
            'id': artifact['id'],
            'name': artifact['name'],
            'description': artifact['description'],
            'image_path': artifact['image_path'],
            'audio_path': artifact['audio_path'],
            'video_path': artifact['video_path'],
            'status': artifact['status']
        })

    return jsonify(artifact_list)

@bp.route('/<int:id>', methods=['GET'])
def get_artifact(id):
    conn = db_connection()
    cursor = conn.cursor()
    artifact = cursor.execute('SELECT * FROM artifact WHERE id = ?', (id,)).fetchone()
    conn.close()

    if artifact:
        return jsonify({
            'id': artifact['id'],
            'name': artifact['name'],
            'description': artifact['description'],
            'image_path': artifact['image_path'],
            'audio_path': artifact['audio_path'],
            'video_path': artifact['video_path'],
            'status': artifact['status']
        })
    else:
        return jsonify({'error': 'Artifact not found'}), 404


@bp.route('/', methods=['POST'])
def create_artifact():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name')
    description = data.get('description')
    image_path = data.get('image_path')
    audio_path = data.get('audio_path')
    video_path = data.get('video_path')
    status = data.get('status', 'working')

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            'insert into artifact (name, description, image_path, audio_path, video_path, status) values (?, ?, ?, ?, ?, ?)',
            (name, description, image_path, audio_path, video_path, status)
        )
        conn.commit()
        artifact_id = cursor.lastrowid #getting the id of created artifact
        conn.close()

        return jsonify({'message': 'Artifact created', 'id': artifact_id}), 201
    except sqlite3.Error as e:
        print(f"Error creating artifact: {e}")
        return jsonify({'error': 'Database error'}), 500
    

@bp.route('/<int:id>', methods=['PUT'])
def update_artifact(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    conn = db_connection()
    cursor = conn.cursor()

    try:
        # Fetch the existing artifact data
        cursor.execute('SELECT * FROM artifact WHERE id = ?', (id,))
        artifact = cursor.fetchone()

        if not artifact:
            return jsonify({'error': 'Artifact not found'}), 404

        # Update only the fields provided in the request
        name = data.get('name', artifact['name'])  # Use existing value if not provided
        description = data.get('description', artifact['description'])
        image_path = data.get('image_path', artifact['image_path'])
        audio_path = data.get('audio_path', artifact['audio_path'])
        video_path = data.get('video_path', artifact['video_path'])
        status = data.get('status', artifact['status'])

        cursor.execute(
            'UPDATE artifact SET name = ?, description = ?, image_path = ?, audio_path = ?, video_path = ?, status = ? WHERE id = ?',
            (name, description, image_path, audio_path, video_path, status, id)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Artifact updated'}), 200
    except Exception as e:
        print(f"Error updating artifact: {e}")
        return jsonify({'error': 'Database error'}), 500
    

@bp.route('/<int:id>', methods=['DELETE'])
def delete_artifact(id):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM artifact WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Artifact deleted'}), 200
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    

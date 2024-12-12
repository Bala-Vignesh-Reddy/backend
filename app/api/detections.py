from flask import Blueprint, request, jsonify # type: ignore
from app.models.artifact import db_connection
import sqlite3
import datetime

bp = Blueprint('detections', __name__, url_prefix='/detections')

@bp.route('/', methods=['GET'])
def get_all_detections():
    conn = db_connection()
    cursor = conn.cursor()

    artifact_id = request.args.get('artifact_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = "select * from detection_event"
    parameters = []
    if artifact_id:
        query += " where artifact_id = ?"
        parameters.append(artifact_id)
    
    if start_date:
        query += " and timestamp >= ?"
        parameters.append(start_date)
    
    if end_date:
        query += " and timestamp <= ?"
        parameters.append(end_date)

    detections = cursor.execute(query, parameters).fetchall()
    conn.close()

    detection_list = []
    for detection in detections:
        print(detection)
        detection_list.append({
            'id': detection['id'],
            'artifact_id': detection['artifact_id'],
            'object_detected': detection['object_detected'],
            'timestamp': detection['timestamp'],
            'image_path': detection['image_path']
        })
    
    return jsonify(detection_list)


@bp.route('/stats', methods=['GET'])
def get_detection_stats():
    conn = db_connection()
    cursor = conn.cursor()

    try:
        stats = cursor.execute(
            'select object_detected, count(*) as count from detection_event group by object_detected'
        ).fetchall()

        conn.close()

        stats_data = {}
        for stat in stats:
            stats_data[stat['object_detected']] = stat['count']
        return jsonify(stats_data)
    except Exception as e:
        print(f"Error fetching detection stats: {e}")
        return jsonify({'error': 'Failed to fetch detection stats'}), 500
    

@bp.route('/', methods=['POST'])
def create_detection():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    artifact_id = data.get('artifact_id')
    object_detected = data.get('object_detected')
    timestamp = data.get('timestamp')
    image_path = data.get('image_path')
    
    '''
    #basic data validation
    if not all([object_detected, timestamp, image_path]):
        return jsonify({'error': 'Missing required fields'}), 400
    '''

    # Data validation
    if not all([artifact_id, object_detected, timestamp, image_path]):
        return jsonify({'error': 'Missing required fields'}), 400

    if not isinstance(artifact_id, int) or artifact_id <= 0:
        return jsonify({'error': 'Invalid artifact_id'}), 400

    if not isinstance(object_detected, str) or not object_detected:
        return jsonify({'error': 'Invalid object_detected'}), 400

    try:
        datetime.datetime.fromisoformat(timestamp)
    except ValueError:
        return jsonify({'error': 'Invalid timestamp format'}), 400

    if not isinstance(image_path, str) or not image_path:
        return jsonify({'error': 'Invalid image_path'}), 400
    
    try:
        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO detection_event (artifact_id, object_detected, timestamp, image_path) VALUES (?, ?, ?, ?)',
            (artifact_id, object_detected, timestamp, image_path)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Detection data received'}), 201
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    

"""checking this work as /detections/check
@bp.route('/check')
def main():
    return jsonify({"message":"working"})
    """


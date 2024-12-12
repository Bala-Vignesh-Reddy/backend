from flask import Blueprint, request, jsonify # type: ignore
from app.models.artifact import db_connection
import datetime

bp = Blueprint('maintenance', __name__, url_prefix='/maintenance')

@bp.route('/predict/<int:artifact_id>', methods=['GET'])
def get_prediction(artifact_id):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        # Fetch predictions for the given artifact_id
        predictions = cursor.execute(
            'SELECT * FROM predictive_maintenance WHERE artifact_id = ?', (artifact_id,)
        ).fetchall()

        conn.close()

        prediction_list = []
        for prediction in predictions:
            prediction_result = eval(prediction['prediction_result'])  # Convert string back to dictionary
            prediction_list.append({
                'id': prediction['id'],
                'artifact_id': prediction['artifact_id'],
                'timestamp': prediction['timestamp'],
                'risk_level': prediction_result['risk_level'],
                'predicted_failure_date': prediction_result['predicted_failure_date']
            })

        return jsonify(prediction_list), 200

    except Exception as e:
        print(f"Error fetching predictions: {e}")
        return jsonify({'error': 'Failed to fetch predictions'}), 500

@bp.route('/predict/<int:artifact_id>', methods=['POST'])
def predict_maintenance(artifact_id):
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data provided'}), 400

    temperature = data.get('temperature')
    humidity = data.get('humidity')
    vibration = data.get('vibration')

    # ... (Perform prediction using your model and the input data) ...
    # This is where you'll use your machine learning model to generate a prediction
    # For now, let's simulate a prediction result
    prediction_result = {
        'risk_level': 'low',  # Replace with actual prediction from your model
        'predicted_failure_date': '2025-06-01'  # Replace with actual prediction
    }

    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO predictive_maintenance (artifact_id, timestamp, prediction_result) VALUES (?, ?, ?)',
            (artifact_id, datetime.datetime.now().isoformat(), str(prediction_result))
        )
        conn.commit()
        conn.close()

        return jsonify({'prediction': prediction_result}), 200

    except Exception as e:
        print(f"Error adding prediction: {e}")
        return jsonify({'error': 'Failed to add prediction'}), 500
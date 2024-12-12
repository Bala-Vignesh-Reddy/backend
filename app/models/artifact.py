import sqlite3
import os
import random 
import datetime

def db_connection():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    db_path = os.path.join(project_root, 'test_museum.db')
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path) #create or connect 
    conn.row_factory = sqlite3.Row #access data as dict
    return conn

def delete_tables():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('drop table if exists artifact')
    cursor.execute('drop table if exists detection_event')

def create_tables():
    #Creates the necessary tables
    conn = db_connection()
    cursor = conn.cursor()
    # cursor.execute('CREATE TABLE IF NOT EXISTS test_artifact ( \
    #                id INTEGER PRIMARY KEY AUTOINCREMENT, \
    #                name TEXT NOT NULL, \
    #                description TEXT, \
    #                image_path TEXT, \
    #                video_path TEXT \
    #                )')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artifact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_path TEXT,
            audio_path TEXT,
            video_path TEXT,
            status TEXT DEFAULT 'working'  -- Add status field with a default value
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detection_event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_id INTEGER,
            object_detected TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            image_path TEXT, 
            FOREIGN KEY (artifact_id) REFERENCES artifact(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictive_maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_id INTEGER, 
            timestamp TEXT NOT NULL,
            prediction_result TEXT, -- store the prediction result (json)                   
            FOREIGN KEY (artifact_id) REFERENCES artifact(id) ON DELETE CASCADE        
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artifact_sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_id INTEGER,
            timestamp TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            vibration REAL,
            FOREIGN KEY (artifact_id) REFERENCES artifact(id) on delete cascade
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_id INTEGER,
            timestamp TEXT NOT NULL,
            issue_description TEXT,
            repair_action TEXT,
            FOREIGN KEY (artifact_id) REFERENCES artifact(id) on delete cascade
        )
    ''')
    conn.commit()
    conn.close()

def dummy_artifacts():
    conn = db_connection()
    cursor = conn.cursor()
    artifacts = [
        ("Ancient Vase", "A beautiful vase from the Ming Dynasty.", "images/ancient_vase.jpg", None, None, "working"),
        ("Stone Sculpture", "An intricate sculpture of a lion.", "images/stone_sculpture.jpg", None, "videos/stone_sculpture.mp4", "working"),
        ("Gold Coin", "A rare gold coin from the Roman Empire.", "images/gold_coin.jpg", "audio/gold_coin.mp3", None, "defective"),
        ("Terracotta Army", "A collection of terracotta warriors and horses.", "images/terracotta_army.jpg", None, None, "working"),
        ("Egyptian Mummy", "A well-preserved mummy from ancient Egypt.", "images/egyptian_mummy.jpg", None, None, "missing")
    ]
    cursor.executemany('INSERT INTO artifact (name, description, image_path, audio_path, video_path, status) VALUES (?, ?, ?, ?, ?, ?)', artifacts)

    # Dummy data for detection_event table
    detections = [
        (1, 'person', '2024-11-25T10:00:00Z', 'images/detection_1.jpg'),
        (2, 'object', '2024-11-25T11:30:00Z', 'images/detection_2.jpg'),
        (3, 'person', '2024-11-25T14:15:00Z', 'images/detection_3.jpg'),
        (1, 'animal', '2024-11-26T09:20:00Z', 'images/detection_4.jpg'),
        (4, 'person', '2024-11-26T15:45:00Z', 'images/detection_5.jpg')
    ]
    cursor.executemany('INSERT INTO detection_event (artifact_id, object_detected, timestamp, image_path) VALUES (?, ?, ?, ?)', detections)

    # --- Predictive maintenance data ---
    now = datetime.datetime.now()
    for i in range(1, 6):  # Generate dummy predictions for each artifact
        for _ in range(random.randint(1, 3)):  # Generate 1-3 predictions per artifact
            timestamp = (now - datetime.timedelta(days=random.randint(1, 30))).isoformat()  # Random timestamp within the last 30 days
            prediction_result = {
                'risk_level': random.choice(['low', 'medium', 'high']),
                'predicted_failure_date': (now + datetime.timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d')  # Random date in the future
            }
            cursor.execute('INSERT INTO predictive_maintenance (artifact_id, timestamp, prediction_result) VALUES (?, ?, ?)',
                           (i, timestamp, str(prediction_result)))  # Note: prediction_result is converted to string for SQLite

    # --- Artifact sensor data ---
    for i in range(1, 6):  # Generate dummy sensor data for each artifact
        for _ in range(random.randint(5, 10)):  # Generate 5-10 readings per artifact
            timestamp = (now - datetime.timedelta(days=random.randint(1, 90))).isoformat()  # Random timestamp within the last 90 days
            temperature = round(random.uniform(15, 30), 2)  # Random temperature between 15 and 30 degrees Celsius
            humidity = round(random.uniform(30, 60), 2)  # Random humidity between 30% and 60%
            vibration = round(random.uniform(0, 1), 2)  # Random vibration level between 0 and 1
            cursor.execute('INSERT INTO artifact_sensor_data (artifact_id, timestamp, temperature, humidity, vibration) VALUES (?, ?, ?, ?, ?)',
                           (i, timestamp, temperature, humidity, vibration))

    # --- Maintenance records ---
    maintenance_issues = [
        "Cracked handle", "Chipped paint", "Loose base", "Faded colors", "Corrosion", "Dust accumulation"
    ]
    repair_actions = [
        "Repaired with adhesive", "Restored paint", "Secured base", "Cleaned and re-colored", "Treated for corrosion", "Cleaned and preserved"
    ]
    for i in range(1, 6):  # Generate dummy maintenance records for each artifact
        for _ in range(random.randint(0, 2)):  # Generate 0-2 records per artifact
            timestamp = (now - datetime.timedelta(days=random.randint(90, 365))).isoformat()  # Random timestamp within the last year
            issue = random.choice(maintenance_issues)
            repair = random.choice(repair_actions)
            cursor.execute('INSERT INTO maintenance_records (artifact_id, timestamp, issue_description, repair_action) VALUES (?, ?, ?, ?)',
                           (i, timestamp, issue, repair))

    conn.commit()
    conn.close()


def alter_detection_event_table():
    conn = db_connection()
    cursor = conn.cursor()

    try:
        # Drop the existing foreign key constraint
        cursor.execute("ALTER TABLE detection_event DROP CONSTRAINT fk_artifact_id")  # Replace 'fk_artifact_id' with the actual constraint name if it's different
    except sqlite3.OperationalError:
        # The constraint might not exist, so we can ignore this error
        pass

    try:
        # Add the new foreign key constraint with ON DELETE CASCADE
        cursor.execute("ALTER TABLE detection_event ADD CONSTRAINT fk_artifact_id FOREIGN KEY (artifact_id) REFERENCES artifact(id) ON DELETE CASCADE")
    except sqlite3.OperationalError:
        # The constraint might already exist, so we can ignore this error
        pass

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    dummy_artifacts()




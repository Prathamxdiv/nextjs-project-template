from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime, date
import json
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize database tables"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            with open('database/init.sql', 'r') as file:
                sql_script = file.read()
                # Execute each statement separately
                for statement in sql_script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
            connection.commit()
            cursor.close()
            connection.close()
            print("Database initialized successfully")
    except Error as e:
        print(f"Error initializing database: {e}")

# Authentication Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('history.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
        connection.commit()
        user_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        session['user_id'] = user_id
        session['username'] = username
        
        return jsonify({'message': 'User created successfully', 'user_id': user_id})
        
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login_post():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return jsonify({'message': 'Login successful', 'user_id': user[0]})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# Workout Routes
@app.route('/workout', methods=['POST'])
def add_workout():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        workout_date = data.get('date', str(date.today()))
        workout_day = data.get('workout_day')
        exercise_name = data.get('exercise_name')
        weight = data.get('weight')
        
        if not all([workout_day, exercise_name, weight]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO workouts (user_id, date, workout_day, exercise_name, weight) 
               VALUES (%s, %s, %s, %s, %s)""",
            (user_id, workout_date, workout_day, exercise_name, weight)
        )
        connection.commit()
        workout_id = cursor.lastrowid
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Workout added successfully', 'id': workout_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workouts', methods=['GET'])
def get_workouts():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        workout_date = request.args.get('date', str(date.today()))
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM workouts 
               WHERE user_id = %s AND date = %s 
               ORDER BY workout_day, exercise_name""",
            (user_id, workout_date)
        )
        workouts = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # Convert datetime objects to strings for JSON serialization
        for workout in workouts:
            if workout['date']:
                workout['date'] = workout['date'].strftime('%Y-%m-%d')
            if workout['created_at']:
                workout['created_at'] = workout['created_at'].isoformat()
            if workout['updated_at']:
                workout['updated_at'] = workout['updated_at'].isoformat()
        
        return jsonify(workouts)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workout/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        weight = data.get('weight')
        
        if not weight:
            return jsonify({'error': 'Weight is required'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE workouts SET weight = %s 
               WHERE id = %s AND user_id = %s""",
            (weight, workout_id, user_id)
        )
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Workout not found'}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Workout updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workout/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM workouts WHERE id = %s AND user_id = %s",
            (workout_id, user_id)
        )
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Workout not found'}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Workout deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Water Routes
@app.route('/water', methods=['POST'])
def add_water():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        water_date = data.get('date', str(date.today()))
        liters = data.get('liters', 0.2)  # Default 200ml increment
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        # Check if entry exists for today
        cursor.execute(
            "SELECT liters FROM water WHERE user_id = %s AND date = %s",
            (user_id, water_date)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Update existing entry
            new_liters = existing[0] + liters
            cursor.execute(
                "UPDATE water SET liters = %s WHERE user_id = %s AND date = %s",
                (new_liters, user_id, water_date)
            )
        else:
            # Create new entry
            cursor.execute(
                "INSERT INTO water (user_id, date, liters) VALUES (%s, %s, %s)",
                (user_id, water_date, liters)
            )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Water intake updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/water', methods=['GET'])
def get_water():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        water_date = request.args.get('date', str(date.today()))
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM water WHERE user_id = %s AND date = %s",
            (user_id, water_date)
        )
        water_entry = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if water_entry:
            # Convert datetime objects to strings
            if water_entry['date']:
                water_entry['date'] = water_entry['date'].strftime('%Y-%m-%d')
            if water_entry['created_at']:
                water_entry['created_at'] = water_entry['created_at'].isoformat()
            if water_entry['updated_at']:
                water_entry['updated_at'] = water_entry['updated_at'].isoformat()
            return jsonify(water_entry)
        else:
            return jsonify({'liters': 0.0, 'date': water_date})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/water/<int:water_id>', methods=['PUT'])
def update_water(water_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        liters = data.get('liters')
        
        if liters is None:
            return jsonify({'error': 'Liters value is required'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE water SET liters = %s WHERE id = %s AND user_id = %s",
            (liters, water_id, user_id)
        )
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Water entry not found'}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Water intake updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/water/<int:water_id>', methods=['DELETE'])
def delete_water(water_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        user_id = session['user_id']
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM water WHERE id = %s AND user_id = %s",
            (water_id, user_id)
        )
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Water entry not found'}), 404
        
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Water entry deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get workout splits
@app.route('/api/workout-splits')
def get_workout_splits():
    return jsonify(Config.WORKOUT_SPLITS)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

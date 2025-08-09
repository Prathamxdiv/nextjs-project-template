import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MySQL Database Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'gym_tracker')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Workout splits configuration
    WORKOUT_SPLITS = {
        1: {
            'name': 'Back & Biceps',
            'exercises': [
                'Deadlifts',
                'Pull-ups',
                'Barbell Rows',
                'Lat Pulldowns',
                'Barbell Curls',
                'Hammer Curls',
                'Cable Curls'
            ]
        },
        2: {
            'name': 'Shoulders',
            'exercises': [
                'Overhead Press',
                'Lateral Raises',
                'Front Raises',
                'Rear Delt Flyes',
                'Upright Rows',
                'Shrugs',
                'Face Pulls'
            ]
        },
        3: {
            'name': 'Chest & Triceps',
            'exercises': [
                'Bench Press',
                'Incline Bench Press',
                'Dumbbell Flyes',
                'Dips',
                'Close-Grip Bench Press',
                'Tricep Extensions',
                'Diamond Push-ups'
            ]
        },
        4: {
            'name': 'Legs',
            'exercises': [
                'Squats',
                'Romanian Deadlifts',
                'Leg Press',
                'Leg Curls',
                'Leg Extensions',
                'Calf Raises',
                'Walking Lunges'
            ]
        },
        5: {
            'name': 'Back & Biceps',
            'exercises': [
                'Deadlifts',
                'Pull-ups',
                'Barbell Rows',
                'Lat Pulldowns',
                'Barbell Curls',
                'Hammer Curls',
                'Cable Curls'
            ]
        },
        6: {
            'name': 'Shoulders',
            'exercises': [
                'Overhead Press',
                'Lateral Raises',
                'Front Raises',
                'Rear Delt Flyes',
                'Upright Rows',
                'Shrugs',
                'Face Pulls'
            ]
        },
        7: {
            'name': 'Chest & Triceps',
            'exercises': [
                'Bench Press',
                'Incline Bench Press',
                'Dumbbell Flyes',
                'Dips',
                'Close-Grip Bench Press',
                'Tricep Extensions',
                'Diamond Push-ups'
            ]
        }
    }

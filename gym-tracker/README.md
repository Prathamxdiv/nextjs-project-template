# 🦍 GYM BEAST - Aggressive Gym Progress Tracker 🐉

A full-stack web application for tracking gym workouts and water intake with an aggressive neon purple theme and beast-mode vibes!

## 🔥 Features

### 💪 Workout Tracker
- **7-Day Split System**: Predefined workout splits for optimal training
  - Day 1 & 5: Back & Biceps
  - Day 2 & 6: Shoulders  
  - Day 3 & 7: Chest & Triceps
  - Day 4: Legs
- **Exercise Logging**: Track weight lifted for each exercise
- **Progress Tracking**: Edit and update your lifts
- **Real-time Updates**: Instant feedback on your gains

### 💧 Water Intake Tracker
- **Daily Goal**: 3-liter hydration target
- **Progress Bar**: Visual representation of daily intake
- **Quick Add**: 200ml increments with one click
- **Goal Achievement**: Track your hydration success

### 📊 History & Analytics
- **Complete History**: View all past workouts and water intake
- **Date Filtering**: Filter by day, week, or month
- **Exercise Analytics**: Track your strongest lifts
- **Progress Visualization**: See your beast journey unfold

### 🎨 Aggressive Design
- **Neon Purple Theme**: High-contrast, aggressive styling
- **Beast Graphics**: Gorilla and dragon elements
- **Dark Mode**: Easy on the eyes during intense sessions
- **Responsive**: Works on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### 1. Clone & Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd gym-tracker

# Install Python dependencies
pip install -r requirements.txt
```

### 2. MySQL Database Setup

#### Install MySQL (if not already installed)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# macOS (using Homebrew)
brew install mysql

# Windows: Download from https://dev.mysql.com/downloads/mysql/
```

#### Start MySQL Service
```bash
# Ubuntu/Debian
sudo systemctl start mysql
sudo systemctl enable mysql

# macOS
brew services start mysql

# Windows: Start MySQL service from Services panel
```

#### Create Database
```bash
# Login to MySQL
mysql -u root -p

# Create database and user (optional)
CREATE DATABASE gym_tracker;
CREATE USER 'gym_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON gym_tracker.* TO 'gym_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Initialize Database Tables
```bash
# Run the initialization script
mysql -u root -p gym_tracker < database/init.sql
```

### 3. Environment Configuration

Create/Edit the `.env` file:
```bash
# Copy the example environment file
cp .env.example .env

# Edit with your MySQL credentials
nano .env
```

Update `.env` with your settings:
```env
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=gym_tracker

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### 4. Run the Application
```bash
# Start the Flask server
python app.py
```

The application will be available at: `http://localhost:5000`

## 🏋️ Usage Guide

### First Time Setup
1. **Navigate to** `http://localhost:5000/login`
2. **Create Account**: Click "SIGN UP" tab and create your beast account
3. **Login**: Use your credentials to access the dashboard

### Logging Workouts
1. **Select Training Day**: Choose from the 7-day split dropdown
2. **Enter Weights**: Input the weight lifted for each exercise
3. **Save Progress**: Click "SAVE" for each exercise
4. **Track Progress**: View your gains in real-time

### Water Tracking
1. **Daily Goal**: Aim for 3 liters per day
2. **Quick Add**: Click the "+" button to add 200ml
3. **Progress Bar**: Watch your hydration level increase
4. **Goal Achievement**: Celebrate when you hit 100%!

### Viewing History
1. **Navigate**: Click "HISTORY" in the navigation
2. **Filter Data**: Use filters to view specific periods
3. **Analytics**: Check your beast statistics
4. **Edit/Delete**: Manage your historical data

## 🛠️ Technical Details

### Backend Stack
- **Flask**: Python web framework
- **MySQL**: Relational database
- **bcrypt**: Password hashing
- **mysql-connector-python**: Database connectivity

### Frontend Stack
- **HTML5**: Semantic markup
- **CSS3**: Aggressive neon styling with animations
- **Vanilla JavaScript**: Dynamic interactions
- **Google Fonts**: Orbitron & Rajdhani fonts

### Database Schema
```sql
-- Users table
users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP
)

-- Workouts table
workouts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT FOREIGN KEY,
    date DATE,
    workout_day INT,
    exercise_name VARCHAR(100),
    weight DECIMAL(5,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)

-- Water intake table
water (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT FOREIGN KEY,
    date DATE,
    liters DECIMAL(3,1),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### API Endpoints

#### Authentication
- `POST /signup` - Create new user account
- `POST /login` - User authentication
- `POST /logout` - End user session

#### Workouts
- `POST /workout` - Log new workout
- `GET /workouts` - Get user workouts (with date filter)
- `PUT /workout/<id>` - Update workout weight
- `DELETE /workout/<id>` - Delete workout entry

#### Water Intake
- `POST /water` - Add water intake
- `GET /water` - Get water intake (with date filter)
- `PUT /water/<id>` - Update water amount
- `DELETE /water/<id>` - Delete water entry

#### Utility
- `GET /api/workout-splits` - Get predefined workout splits

## 🔧 Troubleshooting

### Common Issues

#### MySQL Connection Error
```bash
# Check MySQL service status
sudo systemctl status mysql

# Restart MySQL service
sudo systemctl restart mysql

# Check MySQL credentials in .env file
```

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### Database Tables Not Created
```bash
# Manually run the SQL script
mysql -u root -p gym_tracker < database/init.sql

# Check if tables exist
mysql -u root -p -e "USE gym_tracker; SHOW TABLES;"
```

#### Python Dependencies Issues
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Workout Split Details

### Day 1 & 5: Back & Biceps
- Deadlifts
- Pull-ups
- Barbell Rows
- Lat Pulldowns
- Barbell Curls
- Hammer Curls
- Cable Curls

### Day 2 & 6: Shoulders
- Overhead Press
- Lateral Raises
- Front Raises
- Rear Delt Flyes
- Upright Rows
- Shrugs
- Face Pulls

### Day 3 & 7: Chest & Triceps
- Bench Press
- Incline Bench Press
- Dumbbell Flyes
- Dips
- Close-Grip Bench Press
- Tricep Extensions
- Diamond Push-ups

### Day 4: Legs
- Squats
- Romanian Deadlifts
- Leg Press
- Leg Curls
- Leg Extensions
- Calf Raises
- Walking Lunges

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **Session Management**: Flask sessions
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: Frontend and backend validation
- **CSRF Protection**: Built-in Flask security

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Use production-grade secrets
2. **Database**: Use managed MySQL service
3. **HTTPS**: Enable SSL/TLS encryption
4. **Reverse Proxy**: Use Nginx or Apache
5. **Process Manager**: Use Gunicorn or uWSGI

### Example Production Setup
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/beast-mode`)
3. Commit changes (`git commit -am 'Add beast feature'`)
4. Push to branch (`git push origin feature/beast-mode`)
5. Create Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💪 Beast Mode Activated!

Remember: **"THE PAIN YOU FEEL TODAY WILL BE THE STRENGTH YOU FEEL TOMORROW"**

🦍 PUSH YOUR LIMITS • 🔥 BREAK YOUR RECORDS • ⚡ UNLEASH THE BEAST

---

**Built with 💜 and 🔥 for all the gym beasts out there!**

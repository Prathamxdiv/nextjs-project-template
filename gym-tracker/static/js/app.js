// Global variables
let currentUser = null;
let workoutSplits = {};
let currentDate = new Date().toISOString().split('T')[0];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadWorkoutSplits();
    checkAuthStatus();
    initializeEventListeners();
});

// Check if user is authenticated
function checkAuthStatus() {
    const currentPage = window.location.pathname;
    const isLoginPage = currentPage.includes('login') || currentPage === '/';
    
    // For now, we'll assume user is logged in if not on login page
    // In a real app, you'd check session/token
    if (!isLoginPage) {
        loadDashboard();
    }
}

// Load workout splits from API
async function loadWorkoutSplits() {
    try {
        const response = await fetch('/api/workout-splits');
        workoutSplits = await response.json();
    } catch (error) {
        console.error('Error loading workout splits:', error);
    }
}

// Initialize event listeners
function initializeEventListeners() {
    // Auth form listeners
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
    
    // Auth tab switching
    const authTabs = document.querySelectorAll('.auth-tab');
    authTabs.forEach(tab => {
        tab.addEventListener('click', switchAuthTab);
    });
    
    // Workout day selector
    const workoutDaySelect = document.getElementById('workoutDay');
    if (workoutDaySelect) {
        workoutDaySelect.addEventListener('change', loadWorkoutDay);
    }
    
    // Water tracker button
    const addWaterBtn = document.getElementById('addWaterBtn');
    if (addWaterBtn) {
        addWaterBtn.addEventListener('click', addWater);
    }
    
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
}

// Authentication functions
async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const loginData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    try {
        showLoading('loginBtn');
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        } else {
            showMessage(result.error || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    } finally {
        hideLoading('loginBtn', 'LOGIN');
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const signupData = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    
    const confirmPassword = formData.get('confirmPassword');
    if (signupData.password !== confirmPassword) {
        showMessage('Passwords do not match', 'error');
        return;
    }
    
    try {
        showLoading('signupBtn');
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(signupData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Account created successfully! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        } else {
            showMessage(result.error || 'Signup failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    } finally {
        hideLoading('signupBtn', 'SIGN UP');
    }
}

async function handleLogout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST'
        });
        
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

// Switch between login and signup tabs
function switchAuthTab(e) {
    const tabName = e.target.dataset.tab;
    
    // Update active tab
    document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    e.target.classList.add('active');
    
    // Show/hide forms
    document.querySelectorAll('.auth-form').forEach(form => {
        form.style.display = 'none';
    });
    document.getElementById(tabName + 'Form').style.display = 'block';
}

// Dashboard functions
async function loadDashboard() {
    await loadTodayWorkouts();
    await loadTodayWater();
}

// Workout functions
function loadWorkoutDay() {
    const selectedDay = document.getElementById('workoutDay').value;
    if (!selectedDay || !workoutSplits[selectedDay]) return;
    
    const split = workoutSplits[selectedDay];
    const exercisesContainer = document.getElementById('exercisesContainer');
    
    exercisesContainer.innerHTML = `
        <h3 class="workout-split-title">Day ${selectedDay}: ${split.name}</h3>
        <div class="workout-grid">
            ${split.exercises.map(exercise => `
                <div class="exercise-item">
                    <div class="exercise-name">${exercise}</div>
                    <div class="weight-input">
                        <input 
                            type="number" 
                            placeholder="Weight" 
                            step="0.5" 
                            min="0"
                            id="weight-${exercise.replace(/\s+/g, '-').toLowerCase()}"
                            data-exercise="${exercise}"
                            data-day="${selectedDay}"
                        >
                        <span class="weight-unit">KG</span>
                        <button class="btn btn-small" onclick="saveWorkout('${exercise}', ${selectedDay})">
                            SAVE
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    // Load existing workouts for this day
    loadWorkoutsForDay(selectedDay);
}

async function loadWorkoutsForDay(day) {
    try {
        const response = await fetch(`/workouts?date=${currentDate}`);
        const workouts = await response.json();
        
        workouts.forEach(workout => {
            if (workout.workout_day == day) {
                const inputId = `weight-${workout.exercise_name.replace(/\s+/g, '-').toLowerCase()}`;
                const input = document.getElementById(inputId);
                if (input) {
                    input.value = workout.weight;
                    input.dataset.workoutId = workout.id;
                }
            }
        });
    } catch (error) {
        console.error('Error loading workouts:', error);
    }
}

async function loadTodayWorkouts() {
    try {
        const response = await fetch(`/workouts?date=${currentDate}`);
        const workouts = await response.json();
        
        // Update workout summary if exists
        const workoutSummary = document.getElementById('workoutSummary');
        if (workoutSummary) {
            const workoutCount = workouts.length;
            workoutSummary.innerHTML = `
                <h4>Today's Progress</h4>
                <p>${workoutCount} exercises logged</p>
            `;
        }
    } catch (error) {
        console.error('Error loading today\'s workouts:', error);
    }
}

async function saveWorkout(exerciseName, workoutDay) {
    const inputId = `weight-${exerciseName.replace(/\s+/g, '-').toLowerCase()}`;
    const input = document.getElementById(inputId);
    const weight = parseFloat(input.value);
    
    if (!weight || weight <= 0) {
        showMessage('Please enter a valid weight', 'error');
        return;
    }
    
    const workoutData = {
        date: currentDate,
        workout_day: workoutDay,
        exercise_name: exerciseName,
        weight: weight
    };
    
    try {
        const workoutId = input.dataset.workoutId;
        let response;
        
        if (workoutId) {
            // Update existing workout
            response = await fetch(`/workout/${workoutId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ weight: weight })
            });
        } else {
            // Create new workout
            response = await fetch('/workout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(workoutData)
            });
        }
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage(`${exerciseName} saved successfully!`, 'success');
            if (!workoutId && result.id) {
                input.dataset.workoutId = result.id;
            }
            loadTodayWorkouts(); // Refresh summary
        } else {
            showMessage(result.error || 'Failed to save workout', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

// Water tracking functions
async function loadTodayWater() {
    try {
        const response = await fetch(`/water?date=${currentDate}`);
        const waterData = await response.json();
        
        const currentLiters = waterData.liters || 0;
        const goalLiters = 3.0; // 3 liters goal
        const percentage = Math.min((currentLiters / goalLiters) * 100, 100);
        
        // Update water display
        const waterAmount = document.getElementById('waterAmount');
        const waterProgressBar = document.getElementById('waterProgressBar');
        
        if (waterAmount) {
            waterAmount.textContent = `${currentLiters.toFixed(1)}L / ${goalLiters}L`;
        }
        
        if (waterProgressBar) {
            waterProgressBar.style.width = `${percentage}%`;
        }
        
        // Store water ID for updates
        if (waterData.id) {
            document.getElementById('addWaterBtn').dataset.waterId = waterData.id;
        }
    } catch (error) {
        console.error('Error loading water data:', error);
    }
}

async function addWater() {
    const increment = 0.2; // 200ml
    
    try {
        const response = await fetch('/water', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: currentDate,
                liters: increment
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Water intake updated! +200ml', 'success');
            loadTodayWater(); // Refresh display
        } else {
            showMessage(result.error || 'Failed to update water intake', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

// History functions
async function loadHistory() {
    try {
        // Load workout history
        const workoutResponse = await fetch('/workouts');
        const workouts = await workoutResponse.json();
        
        // Load water history
        const waterResponse = await fetch('/water');
        const waterData = await waterResponse.json();
        
        displayHistory(workouts, waterData);
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function displayHistory(workouts, waterData) {
    const historyContainer = document.getElementById('historyContainer');
    if (!historyContainer) return;
    
    // Group data by date
    const groupedData = {};
    
    workouts.forEach(workout => {
        const date = workout.date;
        if (!groupedData[date]) {
            groupedData[date] = { workouts: [], water: null };
        }
        groupedData[date].workouts.push(workout);
    });
    
    // Add water data
    if (Array.isArray(waterData)) {
        waterData.forEach(water => {
            const date = water.date;
            if (!groupedData[date]) {
                groupedData[date] = { workouts: [], water: null };
            }
            groupedData[date].water = water;
        });
    }
    
    // Sort dates in descending order
    const sortedDates = Object.keys(groupedData).sort((a, b) => new Date(b) - new Date(a));
    
    historyContainer.innerHTML = sortedDates.map(date => {
        const data = groupedData[date];
        return `
            <div class="history-item">
                <div class="history-date">${formatDate(date)}</div>
                <div class="history-content">
                    ${data.workouts.length > 0 ? `
                        <div class="history-workouts">
                            <h4>Workouts (${data.workouts.length} exercises)</h4>
                            <div class="workout-list">
                                ${data.workouts.map(w => `
                                    <div class="workout-entry">
                                        <span>${w.exercise_name}: ${w.weight}kg</span>
                                        <button class="btn btn-small btn-danger" onclick="deleteWorkout(${w.id})">
                                            DELETE
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                    ${data.water ? `
                        <div class="history-water">
                            <h4>Water Intake: ${data.water.liters}L</h4>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

async function deleteWorkout(workoutId) {
    if (!confirm('Are you sure you want to delete this workout?')) return;
    
    try {
        const response = await fetch(`/workout/${workoutId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Workout deleted successfully', 'success');
            loadHistory(); // Refresh history
        } else {
            const result = await response.json();
            showMessage(result.error || 'Failed to delete workout', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

// Utility functions
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at top of main content
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function showLoading(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.innerHTML = '<span class="loading"></span>';
        button.disabled = true;
    }
}

function hideLoading(buttonId, originalText) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Initialize history page if we're on it
if (window.location.pathname.includes('history')) {
    document.addEventListener('DOMContentLoaded', loadHistory);
}

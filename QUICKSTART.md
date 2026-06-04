# Quick Start Guide

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python 3.8+ installed
- ✅ MySQL server running
- ✅ MongoDB server running

## Option 1: Automated Setup (Recommended)

### First Time Setup

1. **Run the setup script** (this will setup databases, install dependencies, and load sample data):
   ```bash
   setup.bat
   ```

2. **Start the application**:
   ```bash
   start_app.bat
   ```

3. **Access the application**:
   - Frontend: http://localhost:8000
   - Backend API: http://localhost:5000

## Option 2: Manual Setup

### Step 1: Setup Databases

**MySQL:**
```bash
mysql -u root -p
# Enter your MySQL password
# Then run:
source database/mysql_schema.sql
exit
```

**MongoDB:**
```bash
mongosh < database/mongodb_setup.js
```

### Step 2: Install Python Dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Setup Sample Data & Train ML Models

```bash
python setup_data.py
```

This will:
- Train the fake review detection model
- Load 10 sample restaurants
- Load sample reviews with sentiment analysis
- Takes about 1-2 minutes

### Step 4: Start Backend Server

```bash
python app.py
```

Backend will run on: http://localhost:5000

### Step 5: Start Frontend

Open a new terminal:

```bash
cd frontend
python -m http.server 8000
```

Or simply open `frontend/index.html` in your browser.

Frontend will run on: http://localhost:8000

## Testing the Application

1. **Visit the landing page**: http://localhost:8000
2. **Sign up** for a new account
3. **Set your preferences** (cuisines, mood, budget)
4. **Get recommendations** - AI will suggest restaurants based on your preferences
5. **View restaurant details** and read authentic reviews
6. **Submit a review** - it will be automatically analyzed for sentiment and authenticity

## Sample Login (if you want to skip signup)

After running `setup_data.py`, you can create a test user:

```bash
# In Python console or add to setup_data.py
from models.user import User
User.create("Test User", "test@example.com", "password123", "+1234567890")
```

Then login with:
- Email: test@example.com
- Password: password123

## Troubleshooting

### MySQL Connection Error
- Make sure MySQL is running
- Check credentials in `backend/config.py`
- Default: user=root, password='' (empty)

### MongoDB Connection Error
- Make sure MongoDB is running
- Default connection: mongodb://localhost:27017/

### Port Already in Use
- Backend (5000): Change in `backend/app.py`
- Frontend (8000): Use different port: `python -m http.server 9000`

### ML Model Training Issues
- Make sure you have enough disk space
- Check Python version (3.8+)
- Reinstall scikit-learn: `pip install --upgrade scikit-learn`

## API Endpoints

Once backend is running, visit:
- http://localhost:5000 - API info
- http://localhost:5000/api/health - Health check
- http://localhost:5000/api/restaurants - List restaurants
- http://localhost:5000/api/restaurants/popular - Popular restaurants

## Next Steps

1. Explore the landing page features
2. Create an account and set preferences
3. Get personalized recommendations
4. Submit reviews and see AI analysis
5. Check the [README.md](README.md) for full documentation

## Stopping the Application

If using `start_app.bat`:
- Press any key in the terminal to stop all servers

If running manually:
- Press `Ctrl+C` in each terminal window

---

**Need Help?** Check the full [README.md](README.md) for detailed documentation.

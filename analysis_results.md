# Why the App Fails to Run Locally

If the application isn't running properly on your machine outside of this environment, it's likely due to one of the following reasons:

### 1. Missing Database Services
The app relies on two database systems that must be installed and running as background services:
- **MySQL** (Port 3306): Used for user authentication and restaurant data.
- **MongoDB** (Port 27017): Used for storing and analyzing reviews.
> [!IMPORTANT]
> If these services aren't started, the backend server will fail to connect and may crash.

### 2. The Setup Process
You must run the `setup.bat` file once before your first run. This script:
- Installs all required Python libraries (like `Flask`, `pandas`, `scikit-learn`).
- Initializes the MySQL database schema.
- Trains the ML models for sentiment analysis and fake review detection.
- Generates the initial sample data.

### 3. Running the Servers Correctly
You cannot simply double-click `frontend/index.html`. Doing so uses the `file://` protocol, which modern browsers block for security reasons when trying to talk to an API (CORS).
- **Correct way**: Run `start_app.bat`. This starts a real web server for the frontend on `http://localhost:8000` and the backend on `http://localhost:5000`.

### 4. MySQL Credentials
The app is configured in `backend/config.py` to use:
- **User**: `root`
- **Password**: `root`
If your local MySQL uses a different password (or no password), you must update `backend/config.py` to match your settings.

### 6. Hardcoded Artifact Paths
In `backend/data/sample_restaurants.json` (and the generator script), many images have paths like:
`"/C:/Users/sruja/.gemini/antigravity/brain/.../image.png"`
These paths point to internal temporary directories used by the AI assistant.
- **Problem**: These folders won't exist if you move the code to another computer or a different user account.
- **Solution**: You should move these images into a dedicated `frontend/assets/images` folder and update the JSON to use relative paths (e.g., `"assets/images/image.png"`).

FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download required NLTK data for TextBlob / NLTK
RUN python -m nltk.downloader punkt wordnet

# Copy all backend files
COPY . .

# Expose port
EXPOSE 5000

# Start command (wait for databases, run migrations, seed data, and start server)
CMD ["sh", "-c", "python wait_for_db.py && python setup_mysql.py && python setup_data.py && gunicorn --bind 0.0.0.0:5000 'app:create_app()'"]

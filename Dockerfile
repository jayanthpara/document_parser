# Step 1: Use Python base image
FROM python:3.9-slim

# Step 2: Set work directory
WORKDIR /app

# Step 3: Copy project files
COPY . /app

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Download NLTK data (punkt) without internet later
RUN python -m nltk.downloader punkt

# Step 6: Set command to run your script
CMD ["python", "main.py"]

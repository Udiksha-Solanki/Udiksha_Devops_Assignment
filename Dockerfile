# Use official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy requirement packages first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else (app + model files) into the container
COPY . .

# Copy model.pkl and label_encoders.pkl to the app directory
COPY model.pkl /app/model.pkl
COPY label_encoders.pkl /app/label_encoders.pkl

# Expose FastAPI default port
EXPOSE 1000

# Command to run the FastAPI server
CMD ["uvicorn", "main_:app", "--host", "0.0.0.0", "--port", "1000"]

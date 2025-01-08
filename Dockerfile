# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install flask redis

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
